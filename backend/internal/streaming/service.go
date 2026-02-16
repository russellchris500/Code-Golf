package streaming

import (
	"context"
	"io"
	"log"

	"github.com/google/uuid"
	pb "github.com/yourusername/agent/backend/pb/streaming"
	"github.com/yourusername/agent/backend/internal/relay"
)

type Service struct {
	pb.UnimplementedStreamingServiceServer
	relay *relay.RelayManager
}

func NewService(relayManager *relay.RelayManager) *Service {
	return &Service{
		relay: relayManager,
	}
}

func (s *Service) RegisterDevice(ctx context.Context, req *pb.RegisterRequest) (*pb.RegisterResponse, error) {
	log.Printf("Device registration request: user=%s, type=%s", req.UserId, req.DeviceType)

	sessionID := uuid.New().String()

	pairingInfo := s.relay.GetPairingInfo(req.UserId)

	return &pb.RegisterResponse{
		Success:     true,
		SessionId:   sessionID,
		PairingInfo: pairingInfo,
	}, nil
}

func (s *Service) GetPairingStatus(ctx context.Context, req *pb.PairingStatusRequest) (*pb.PairingStatusResponse, error) {
	pairingInfo := s.relay.GetPairingInfo(req.UserId)

	paired := pairingInfo.DesktopOnline && pairingInfo.MobileOnline

	return &pb.PairingStatusResponse{
		Paired:      paired,
		PairingInfo: pairingInfo,
	}, nil
}

func (s *Service) Stream(stream pb.StreamingService_StreamServer) error {
	var userID string
	var deviceType pb.DeviceType
	registered := false

	defer func() {
		if registered {
			s.relay.UnregisterDevice(userID, deviceType)
			log.Printf("Stream closed for user %s, device %s", userID, deviceType)
		}
	}()

	for {
		packet, err := stream.Recv()
		if err == io.EOF {
			log.Printf("Client closed stream: user=%s, device=%s", userID, deviceType)
			return nil
		}
		if err != nil {
			log.Printf("Error receiving packet: %v", err)
			return err
		}

		// First packet should contain user identification
		if !registered {
			userID = packet.UserId
			deviceType = packet.Source

			if userID == "" {
				log.Printf("Invalid packet: missing user_id")
				continue
			}

			// Register this device stream
			if err := s.relay.RegisterDevice(userID, deviceType, stream); err != nil {
				log.Printf("Failed to register device: %v", err)
				return err
			}
			registered = true

			// Send pairing info back
			pairingInfo := s.relay.GetPairingInfo(userID)
			controlPacket := &pb.Packet{
				PacketId:    uuid.New().String(),
				UserId:      userID,
				Source:      pb.DeviceType_UNKNOWN_DEVICE,
				Destination: deviceType,
				Type:        pb.PacketType_CONTROL,
				Payload: &pb.Packet_Control{
					Control: &pb.ControlMessage{
						ControlType: pb.ControlType_ACK,
						Message:     formatPairingMessage(pairingInfo),
					},
				},
			}
			if err := stream.Send(controlPacket); err != nil {
				log.Printf("Failed to send pairing info: %v", err)
				return err
			}

			log.Printf("Device registered and paired: user=%s, device=%s, pairing=%v",
				userID, deviceType, pairingInfo)
			continue
		}

		// Route packet to destination
		if err := s.relay.RoutePacket(packet); err != nil {
			log.Printf("Failed to route packet: %v", err)

			// Send error back to sender
			errorPacket := &pb.Packet{
				PacketId:    uuid.New().String(),
				UserId:      userID,
				Source:      pb.DeviceType_UNKNOWN_DEVICE,
				Destination: deviceType,
				Type:        pb.PacketType_CONTROL,
				Payload: &pb.Packet_Control{
					Control: &pb.ControlMessage{
						ControlType: pb.ControlType_ERROR,
						Message:     err.Error(),
					},
				},
			}
			if err := stream.Send(errorPacket); err != nil {
				log.Printf("Failed to send error packet: %v", err)
				return err
			}
		}
	}
}

func formatPairingMessage(info *pb.PairingInfo) string {
	if info.DesktopOnline && info.MobileOnline {
		return "Both devices paired"
	} else if info.DesktopOnline {
		return "Desktop online, waiting for mobile"
	} else if info.MobileOnline {
		return "Mobile online, waiting for desktop"
	}
	return "No devices online"
}

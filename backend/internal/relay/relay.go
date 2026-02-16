package relay

import (
	"fmt"
	"log"
	"sync"

	pb "github.com/yourusername/agent/backend/pb/streaming"
)

// DeviceStream represents a connected device stream
type DeviceStream struct {
	UserID     string
	DeviceType pb.DeviceType
	Stream     pb.StreamingService_StreamServer
}

// RelayManager manages connections and routes packets between paired devices
type RelayManager struct {
	mu          sync.RWMutex
	connections map[string]map[pb.DeviceType]*DeviceStream // userID -> deviceType -> stream
}

func NewRelayManager() *RelayManager {
	return &RelayManager{
		connections: make(map[string]map[pb.DeviceType]*DeviceStream),
	}
}

// RegisterDevice registers a device stream
func (rm *RelayManager) RegisterDevice(userID string, deviceType pb.DeviceType, stream pb.StreamingService_StreamServer) error {
	rm.mu.Lock()
	defer rm.mu.Unlock()

	if rm.connections[userID] == nil {
		rm.connections[userID] = make(map[pb.DeviceType]*DeviceStream)
	}

	// Close existing connection if any
	if existing, ok := rm.connections[userID][deviceType]; ok {
		log.Printf("Replacing existing %s connection for user %s", deviceType, userID)
		// Note: The old stream will error out on next send/receive
		_ = existing
	}

	rm.connections[userID][deviceType] = &DeviceStream{
		UserID:     userID,
		DeviceType: deviceType,
		Stream:     stream,
	}

	log.Printf("Registered %s device for user %s", deviceType, userID)
	return nil
}

// UnregisterDevice removes a device stream
func (rm *RelayManager) UnregisterDevice(userID string, deviceType pb.DeviceType) {
	rm.mu.Lock()
	defer rm.mu.Unlock()

	if rm.connections[userID] != nil {
		delete(rm.connections[userID], deviceType)
		log.Printf("Unregistered %s device for user %s", deviceType, userID)

		// Clean up empty user map
		if len(rm.connections[userID]) == 0 {
			delete(rm.connections, userID)
		}
	}
}

// RoutePacket routes a packet from source to destination device
func (rm *RelayManager) RoutePacket(packet *pb.Packet) error {
	rm.mu.RLock()
	defer rm.mu.RUnlock()

	userConns, ok := rm.connections[packet.UserId]
	if !ok {
		return fmt.Errorf("no connections for user %s", packet.UserId)
	}

	// Get destination stream
	destStream, ok := userConns[packet.Destination]
	if !ok {
		return fmt.Errorf("destination device %s not connected for user %s", packet.Destination, packet.UserId)
	}

	// Send packet to destination
	if err := destStream.Stream.Send(packet); err != nil {
		log.Printf("Error sending packet to %s for user %s: %v", packet.Destination, packet.UserId, err)
		return err
	}

	log.Printf("Routed packet from %s to %s for user %s (type: %s)",
		packet.Source, packet.Destination, packet.UserId, packet.Type)
	return nil
}

// GetPairingInfo returns information about connected devices for a user
func (rm *RelayManager) GetPairingInfo(userID string) *pb.PairingInfo {
	rm.mu.RLock()
	defer rm.mu.RUnlock()

	info := &pb.PairingInfo{
		DesktopOnline: false,
		MobileOnline:  false,
	}

	if userConns, ok := rm.connections[userID]; ok {
		if _, ok := userConns[pb.DeviceType_DESKTOP]; ok {
			info.DesktopOnline = true
		}
		if _, ok := userConns[pb.DeviceType_MOBILE]; ok {
			info.MobileOnline = true
		}
	}

	return info
}

// BroadcastToUser sends a packet to all connected devices for a user
func (rm *RelayManager) BroadcastToUser(userID string, packet *pb.Packet) error {
	rm.mu.RLock()
	defer rm.mu.RUnlock()

	userConns, ok := rm.connections[userID]
	if !ok {
		return fmt.Errorf("no connections for user %s", userID)
	}

	var lastErr error
	for deviceType, stream := range userConns {
		if err := stream.Stream.Send(packet); err != nil {
			log.Printf("Error broadcasting to %s for user %s: %v", deviceType, userID, err)
			lastErr = err
		}
	}

	return lastErr
}

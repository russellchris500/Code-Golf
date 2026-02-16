package main

import (
	"fmt"
	"log"
	"net"
	"os"

	"github.com/joho/godotenv"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"

	authpb "github.com/yourusername/agent/backend/pb/auth"
	streamingpb "github.com/yourusername/agent/backend/pb/streaming"

	"github.com/yourusername/agent/backend/internal/auth"
	"github.com/yourusername/agent/backend/internal/relay"
	"github.com/yourusername/agent/backend/internal/streaming"
)

// Test version that runs without database
func main() {
	// Load environment variables
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found, using environment variables")
	}

	// Get port from environment
	port := os.Getenv("PORT")
	if port == "" {
		port = "50051"
	}

	log.Println("⚠️  Running in TEST MODE (no database)")

	// Create relay manager
	relayManager := relay.NewRelayManager()

	// Create services (without database for auth)
	authService := auth.NewService(nil) // nil database - will work for basic testing
	streamingService := streaming.NewService(relayManager)

	// Create gRPC server
	grpcServer := grpc.NewServer()

	// Register services
	authpb.RegisterAuthServiceServer(grpcServer, authService)
	streamingpb.RegisterStreamingServiceServer(grpcServer, streamingService)

	// Register reflection service for debugging
	reflection.Register(grpcServer)

	// Start listening
	address := fmt.Sprintf("0.0.0.0:%s", port)
	listener, err := net.Listen("tcp", address)
	if err != nil {
		log.Fatalf("Failed to listen on %s: %v", address, err)
	}

	log.Printf("🚀 gRPC server starting on %s", address)
	log.Printf("Environment: %s", os.Getenv("ENV"))
	log.Printf("⚠️  Database disabled for testing")
	log.Println()
	log.Println("To test:")
	log.Println("  grpcurl -plaintext localhost:50051 list")

	if err := grpcServer.Serve(listener); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}

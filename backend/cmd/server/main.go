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
	"github.com/yourusername/agent/backend/internal/database"
	"github.com/yourusername/agent/backend/internal/relay"
	"github.com/yourusername/agent/backend/internal/streaming"
)

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

	// Initialize database
	db, err := database.New()
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	// Initialize database schema
	if err := db.InitSchema(); err != nil {
		log.Fatalf("Failed to initialize database schema: %v", err)
	}

	// Create relay manager
	relayManager := relay.NewRelayManager()

	// Create services
	authService := auth.NewService(db)
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

	if err := grpcServer.Serve(listener); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}

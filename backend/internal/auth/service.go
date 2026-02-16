package auth

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
	pb "github.com/yourusername/agent/backend/pb/auth"
	"github.com/yourusername/agent/backend/internal/database"
)

type Service struct {
	pb.UnimplementedAuthServiceServer
	db        *database.DB
	jwtSecret []byte
}

func NewService(db *database.DB) *Service {
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		secret = "default-secret-change-in-production"
		log.Println("WARNING: Using default JWT secret")
	}

	return &Service{
		db:        db,
		jwtSecret: []byte(secret),
	}
}

func (s *Service) AuthenticateOAuth(ctx context.Context, req *pb.OAuthRequest) (*pb.AuthResponse, error) {
	log.Printf("OAuth authentication request: provider=%s, device=%s", req.Provider, req.DeviceType)

	// TODO: Implement actual OAuth token verification with Google/Apple
	// For now, we'll create a simple mock implementation
	// In production, you would:
	// 1. Verify the OAuth token with the provider
	// 2. Extract user info (email, subject)
	// 3. Create or get user from database

	// Mock: Extract email from token (in production, verify with Google)
	email := "user@example.com" // TODO: Extract from verified OAuth token
	subject := "mock-subject-" + req.OauthToken[:min(10, len(req.OauthToken))] // TODO: Get from OAuth provider

	var userID string

	// Create or get user (skip if database not available)
	if s.db != nil {
		user, err := s.db.CreateOrGetUser(email, req.Provider, subject)
		if err != nil {
			return &pb.AuthResponse{
				Success:      false,
				ErrorMessage: fmt.Sprintf("Failed to create user: %v", err),
			}, nil
		}
		userID = user.ID.String()
	} else {
		// Mock mode: generate a test user ID
		userID = uuid.New().String()
		log.Printf("⚠️  TEST MODE: Using mock user ID: %s", userID)
	}

	// Generate JWT
	accessToken, err := s.generateJWT(userID, 24*time.Hour)
	if err != nil {
		return &pb.AuthResponse{
			Success:      false,
			ErrorMessage: fmt.Sprintf("Failed to generate token: %v", err),
		}, nil
	}

	// Generate refresh token
	refreshToken := uuid.New().String()
	// TODO: Store refresh token in database

	return &pb.AuthResponse{
		Success:      true,
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		ExpiresIn:    int64(24 * 3600), // 24 hours in seconds
		UserId:       userID,
	}, nil
}

func (s *Service) RefreshToken(ctx context.Context, req *pb.RefreshRequest) (*pb.AuthResponse, error) {
	// TODO: Implement refresh token validation and rotation
	return &pb.AuthResponse{
		Success:      false,
		ErrorMessage: "Not implemented yet",
	}, nil
}

func (s *Service) ValidateToken(ctx context.Context, req *pb.ValidateRequest) (*pb.ValidateResponse, error) {
	claims, err := s.validateJWT(req.AccessToken)
	if err != nil {
		return &pb.ValidateResponse{
			Valid: false,
		}, nil
	}

	userID, ok := claims["user_id"].(string)
	if !ok {
		return &pb.ValidateResponse{
			Valid: false,
		}, nil
	}

	return &pb.ValidateResponse{
		Valid:  true,
		UserId: userID,
	}, nil
}

func (s *Service) StoreAPIKeys(ctx context.Context, req *pb.StoreAPIKeysRequest) (*pb.StoreAPIKeysResponse, error) {
	// TODO: Encrypt API keys before storing
	// For now, storing as-is (NOT SECURE - implement encryption in production)

	log.Printf("Storing API keys for user %s", req.UserId)

	// TODO: Implement database storage
	return &pb.StoreAPIKeysResponse{
		Success: true,
	}, nil
}

func (s *Service) GetAPIKeys(ctx context.Context, req *pb.GetAPIKeysRequest) (*pb.GetAPIKeysResponse, error) {
	// TODO: Retrieve and decrypt API keys
	log.Printf("Retrieving API keys for user %s", req.UserId)

	// TODO: Implement database retrieval
	return &pb.GetAPIKeysResponse{
		Success: true,
		ApiKeys: make(map[string]string),
	}, nil
}

func (s *Service) generateJWT(userID string, expiration time.Duration) (string, error) {
	claims := jwt.MapClaims{
		"user_id": userID,
		"exp":     time.Now().Add(expiration).Unix(),
		"iat":     time.Now().Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(s.jwtSecret)
}

func (s *Service) validateJWT(tokenString string) (jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return s.jwtSecret, nil
	})

	if err != nil {
		return nil, err
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		return claims, nil
	}

	return nil, fmt.Errorf("invalid token")
}

func hashToken(token string) string {
	hash := sha256.Sum256([]byte(token))
	return hex.EncodeToString(hash[:])
}

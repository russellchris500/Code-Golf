package database

import (
	"database/sql"
	"time"

	"github.com/google/uuid"
)

type User struct {
	ID            uuid.UUID
	Email         string
	OAuthProvider string
	OAuthSubject  string
	CreatedAt     time.Time
	UpdatedAt     time.Time
}

func (db *DB) CreateOrGetUser(email, oauthProvider, oauthSubject string) (*User, error) {
	var user User

	// Try to get existing user
	err := db.QueryRow(`
		SELECT id, email, oauth_provider, oauth_subject, created_at, updated_at
		FROM users
		WHERE oauth_provider = $1 AND oauth_subject = $2
	`, oauthProvider, oauthSubject).Scan(
		&user.ID, &user.Email, &user.OAuthProvider, &user.OAuthSubject,
		&user.CreatedAt, &user.UpdatedAt,
	)

	if err == nil {
		// User exists, update email if changed
		if user.Email != email {
			_, err = db.Exec(`
				UPDATE users SET email = $1, updated_at = NOW()
				WHERE id = $2
			`, email, user.ID)
			if err != nil {
				return nil, err
			}
			user.Email = email
		}
		return &user, nil
	}

	if err != sql.ErrNoRows {
		return nil, err
	}

	// Create new user
	err = db.QueryRow(`
		INSERT INTO users (email, oauth_provider, oauth_subject)
		VALUES ($1, $2, $3)
		RETURNING id, email, oauth_provider, oauth_subject, created_at, updated_at
	`, email, oauthProvider, oauthSubject).Scan(
		&user.ID, &user.Email, &user.OAuthProvider, &user.OAuthSubject,
		&user.CreatedAt, &user.UpdatedAt,
	)

	return &user, err
}

func (db *DB) GetUserByID(userID uuid.UUID) (*User, error) {
	var user User
	err := db.QueryRow(`
		SELECT id, email, oauth_provider, oauth_subject, created_at, updated_at
		FROM users
		WHERE id = $1
	`, userID).Scan(
		&user.ID, &user.Email, &user.OAuthProvider, &user.OAuthSubject,
		&user.CreatedAt, &user.UpdatedAt,
	)
	if err != nil {
		return nil, err
	}
	return &user, nil
}

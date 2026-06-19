from datetime import datetime

from app.database import SessionLocal
from app.models.refresh_token_model import RefreshToken
from app.models.email_verification_token_model import EmailVerificationToken
from app.models.password_reset_model_token import PasswordResetToken


def cleanup_tokens():
    db = SessionLocal()

    try:
        now = datetime.utcnow()

        deleted_refresh_tokens = db.query(RefreshToken).filter(
            (RefreshToken.is_revoked == True) |
            (RefreshToken.expires_at < now)
        ).delete(synchronize_session=False)

        deleted_email_verification_tokens = db.query(EmailVerificationToken).filter(
            (EmailVerificationToken.is_used == True) |
            (EmailVerificationToken.expires_at < now)
        ).delete(synchronize_session=False)

        deleted_password_reset_tokens = db.query(PasswordResetToken).filter(
            (PasswordResetToken.is_used == True) |
            (PasswordResetToken.expires_at < now)
        ).delete(synchronize_session=False)

        db.commit()

        print("Token cleanup completed successfully.")
        print(f"Deleted refresh tokens: {deleted_refresh_tokens}")
        print(f"Deleted email verification tokens: {deleted_email_verification_tokens}")
        print(f"Deleted password reset tokens: {deleted_password_reset_tokens}")

    except Exception as error:
        db.rollback()
        print(f"Something went wrong during token cleanup: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    cleanup_tokens()
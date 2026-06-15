from getpass import getpass

from app.database import SessionLocal
from app.models.uer_models import User
from app.security import hash_password


def create_admin():
    db = SessionLocal()

    try:
        print("Create or promote admin user")
        print("-" * 30)

        name = input("Enter admin name: ").strip()
        email = input("Enter admin email: ").strip().lower()
        age = input("Enter admin age: ").strip()

        existing_user = db.query(User).filter(
            User.email == email
        ).first()

        if existing_user:
            existing_user.role = "admin"
            existing_user.is_deleted = False
            existing_user.deleted_at = None

            db.commit()

            print("Existing user promoted to admin successfully.")
            return

        password = getpass("Enter admin password: ").strip()
        confirm_password = getpass("Confirm admin password: ").strip()

        if password != confirm_password:
            print("Passwords do not match.")
            return

        if len(password) < 6:
            print("Password must be at least 6 characters long.")
            return

        admin_user = User(
            name=name,
            email=email,
            age=int(age),
            password=hash_password(password),
            role="admin",
            is_deleted=False
        )

        db.add(admin_user)
        db.commit()

        print("Admin user created successfully.")

    except ValueError:
        print("Age must be a valid number.")

    except Exception as error:
        db.rollback()
        print(f"Something went wrong: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
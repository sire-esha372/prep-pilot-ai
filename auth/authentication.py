import bcrypt
from datetime import datetime
from database.mongodb import get_users_collection


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_user(name, email, password):
    users = get_users_collection()

    existing_user = users.find_one({
        "email": email.lower().strip()
    })

    if existing_user:
        return False, "An account with this email already exists."

    user = {
        "name": name.strip(),
        "email": email.lower().strip(),
        "password_hash": hash_password(password),
        "created_at": datetime.utcnow()
    }

    users.insert_one(user)

    return True, "Account created successfully."


def authenticate_user(email, password):
    users = get_users_collection()

    user = users.find_one({
        "email": email.lower().strip()
    })

    if not user:
        return None

    if verify_password(password, user["password_hash"]):
        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }

    return None
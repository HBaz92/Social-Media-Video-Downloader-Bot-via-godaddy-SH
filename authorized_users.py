import os
import json
import logging

# File to store authorized users
AUTH_FILE = "authorized_users.json"

# Initialize with your own Telegram ID as admin
DEFAULT_ADMIN = 123456789  # Replace with your actual Telegram ID


def load_authorized_users():
    """Load the list of authorized user IDs"""
    try:
        if os.path.exists(AUTH_FILE):
            with open(AUTH_FILE, "r") as f:
                data = json.load(f)
                return data.get("users", []), data.get("admins", [DEFAULT_ADMIN])
        else:
            # Create default file with you as admin
            users = []
            admins = [DEFAULT_ADMIN]
            save_authorized_users(users, admins)
            return users, admins
    except Exception as e:
        logging.error(f"Error loading authorized users: {e}")
        return [], [DEFAULT_ADMIN]


def save_authorized_users(users, admins):
    """Save the list of authorized users"""
    try:
        with open(AUTH_FILE, "w") as f:
            json.dump({"users": users, "admins": admins}, f)
        return True
    except Exception as e:
        logging.error(f"Error saving authorized users: {e}")
        return False


def is_authorized(user_id):
    """Check if a user is authorized"""
    users, admins = load_authorized_users()
    return user_id in users or user_id in admins


def is_admin(user_id):
    """Check if a user is an admin"""
    _, admins = load_authorized_users()
    return user_id in admins


def add_user(user_id, added_by=None):
    """Add a user to the authorized list"""
    users, admins = load_authorized_users()
    if user_id not in users:
        users.append(user_id)
        save_authorized_users(users, admins)
        logging.info(f"User {user_id} added by {added_by}")
        return True
    return False


def remove_user(user_id, removed_by=None):
    """Remove a user from the authorized list"""
    users, admins = load_authorized_users()
    if user_id in users:
        users.remove(user_id)
        save_authorized_users(users, admins)
        logging.info(f"User {user_id} removed by {removed_by}")
        return True
    return False

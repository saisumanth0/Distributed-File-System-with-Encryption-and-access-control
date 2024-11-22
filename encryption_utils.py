from cryptography.fernet import Fernet

def generate_key():
    """Generates and returns a new encryption key."""
    return Fernet.generate_key()

import random
import string
import uuid


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def generate_api_key() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

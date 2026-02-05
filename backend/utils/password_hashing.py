from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(
    memory_cost=102400,
    time_cost=1,
    parallelism=8
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    except Exception:
        # Log unexpected errors if possible, or just return False to be safe
        return False

def hash_password(password: str) -> str:
    return ph.hash(password)

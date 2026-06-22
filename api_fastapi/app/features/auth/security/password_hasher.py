from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

class PasswordHasher:
    def __init__(self):
        self.pwd_context = PasswordHash(
            hashers=[Argon2Hasher()],
        )

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
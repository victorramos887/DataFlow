from pwdlib import PasswordHash

class PasswordHasher:
    def __init__(self):
        self.pwd_context = PasswordHash()

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
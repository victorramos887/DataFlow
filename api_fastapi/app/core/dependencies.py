import hashlib

from app.features.auth.entities.user_entity import User
from app.features.auth.service.auth_service import AuthService


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: list[User] = []
        self._next_id = 1

    def get_by_email(self, email: str) -> User | None:
        for user in self._users:
            if user.email == email:
                return user
        return None

    def create(self, user: User) -> User:
        created_user = User(
            id=self._next_id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
        )
        self._users.append(created_user)
        self._next_id += 1
        return created_user


class PasswordHasher:
    def hash(self, raw_password: str) -> str:
        return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


_user_repository = InMemoryUserRepository()
_password_hasher = PasswordHasher()

def get_auth_service() -> AuthService:
    return AuthService(
        user_repository=_user_repository,
        password_hasher=_password_hasher,
    )
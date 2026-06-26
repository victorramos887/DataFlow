import asyncio
import sys
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import settings
from app.features.auth.infra.security.password_hasher import PasswordHasher


ADMIN_EMAIL = "admin@email.com"
ADMIN_PASSWORD = "admin123"
ADMIN_NAME = "Admin"


PERMISSIONS = [
    ("users.create", "Create users"),
    ("users.read", "Read users"),
    ("users.update", "Update users"),
    ("users.delete", "Delete users"),

    ("roles.create", "Create roles"),
    ("roles.read", "Read roles"),
    ("roles.update", "Update roles"),
    ("roles.delete", "Delete roles"),

    ("permissions.create", "Create permissions"),
    ("permissions.read", "Read permissions"),
    ("permissions.update", "Update permissions"),
    ("permissions.delete", "Delete permissions"),
]


async def seed_admin():
    engine = create_async_engine(settings.database_url)
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    password_hasher = PasswordHasher()
    password_hash = password_hasher.hash_password(ADMIN_PASSWORD)

    async with SessionLocal() as session:
        # permissions
        for name, description in PERMISSIONS:
            await session.execute(
                text("""
                    INSERT INTO permissions (name, description)
                    VALUES (:name, :description)
                    ON CONFLICT (name) DO NOTHING
                """),
                {"name": name, "description": description},
            )

        # role admin
        await session.execute(
            text("""
                INSERT INTO roles (name, description)
                VALUES ('admin', 'Administrator role')
                ON CONFLICT (name) DO NOTHING
            """)
        )

        # user admin
        await session.execute(
            text("""
                INSERT INTO users (name, email, password_hash, is_active)
                VALUES (:name, :email, :password_hash, true)
                ON CONFLICT (email) DO NOTHING
            """),
            {
                "name": ADMIN_NAME,
                "email": ADMIN_EMAIL,
                "password_hash": password_hash,
            },
        )

        # link role -> permissions
        await session.execute(
            text("""
                INSERT INTO role_permissions (role_id, permission_id)
                SELECT r.id, p.id
                FROM roles r
                CROSS JOIN permissions p
                WHERE r.name = 'admin'
                ON CONFLICT DO NOTHING
            """)
        )

        # link user -> role
        await session.execute(
            text("""
                INSERT INTO user_roles (user_id, role_id)
                SELECT u.id, r.id
                FROM users u
                JOIN roles r ON r.name = 'admin'
                WHERE u.email = :email
                ON CONFLICT DO NOTHING
            """),
            {"email": ADMIN_EMAIL},
        )

        await session.commit()

    await engine.dispose()

    print("Seed admin created successfully")


if __name__ == "__main__":
    asyncio.run(seed_admin())
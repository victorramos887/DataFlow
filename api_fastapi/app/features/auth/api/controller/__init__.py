from fastapi import APIRouter

from app.features.auth.api.controller import auth_users_controller
from app.features.auth.api.controller import auth_permissions_controller
from app.features.auth.api.controller import auth_roles_controller

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

router.include_router(auth_users_controller.router)
router.include_router(auth_permissions_controller.router)
router.include_router(auth_roles_controller.protected_router)

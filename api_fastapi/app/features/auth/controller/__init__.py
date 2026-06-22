from fastapi import APIRouter

from app.features.auth.controller import auth_controller
from app.features.auth.controller import auth_permissions_controller

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

router.include_router(auth_controller.router)
router.include_router(auth_permissions_controller.router)


from fastapi import APIRouter

from app.features.auth.controller import auth_controller

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

router.include_router(auth_controller.router)


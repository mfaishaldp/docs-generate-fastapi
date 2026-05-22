from fastapi import APIRouter

from app.controllers.user_controller import get_users

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

router.get('/')(get_users)
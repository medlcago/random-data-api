from fastapi import APIRouter

from api.routes import login
from api.routes import random
from api.routes import users
from api.routes import utils

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(random.router, prefix="/random", tags=["Generate random data"])
api_router.include_router(utils.router, tags=["Utils"])

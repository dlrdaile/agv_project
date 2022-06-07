"""
author:dlr123
date:2022年05月31日
"""
from fastapi import APIRouter,Depends

from core.security import get_current_user
from models.user.users import Users
from schemas.user import OutputUser
from utils.resp_code import resp_200

user_api = APIRouter(prefix="/user")


@user_api.get('/userinfo')
async def get_user_info(user: Users = Depends(get_current_user)) :
    data = OutputUser.from_orm(user)
    data.roles = ["admin",] if data.isAdmin else ["client",]
    return resp_200(data=data)

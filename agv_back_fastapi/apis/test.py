"""
author:dlr123
date:2022年05月31日
"""
from fastapi import APIRouter,Depends
from utils.resp_code import resp_200
from crud.user import UserCrud
from schemas.user import UserIn
from utils.custom_exc import UserNotExist
from schemas.token import TokenInfo
from models.user.users import Users
from core.security import get_current_user
from schemas.user import OutputUser
test_api = APIRouter(tags=['test'])

@test_api.post('/')
async def hello_world(userin:UserIn):
    usercrud = UserCrud()
    result = usercrud.authenticate(userin.name,'123456')
    if result:
        out_res = TokenInfo.from_orm(result)
        return resp_200(data=out_res.dict())
    else:
        raise UserNotExist(err_desc=f"{userin.name}不存在")

@test_api.get('/user')
async def get_user_info(user:Users = Depends(get_current_user)):
    return resp_200(data=OutputUser.from_orm(user))

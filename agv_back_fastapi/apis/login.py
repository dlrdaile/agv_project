"""
author:dlr123
date:2022年05月31日
"""
from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm

from core import create_access_token
from crud.user import userCrud
from schemas.token import Token
from schemas.token import TokenInfo
from utils.custom_exc import UserNotExist

login_api = APIRouter()


@login_api.post("/login",response_model=Token,summary="docs接口文档登录 && 登录接口")
async def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()
) :
    """ 兼容OAuth2的令牌登录，为接口文档的请求获取访问令牌 """
    current_user = userCrud.authenticate(form_data.username,form_data.password)
    if current_user is not None :
        token_info = TokenInfo.from_orm(current_user)
        token = create_access_token(token_info.dict())
        # 这里'access_token'和'token_type'一定要写,否则get_current_user依赖拿不到token
        # 可添加字段(先修改schemas/token里面的Token返回模型)
        return {"access_token" : token,"token_type" : "bearer"}
    else :
        raise UserNotExist



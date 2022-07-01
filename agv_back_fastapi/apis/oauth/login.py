"""
author:dlr123
date:2022年05月31日
"""
import datetime

from fastapi import Depends

from apis.oauth import oauth_api
from core import create_access_token
from core.logger import logger
from core.security import get_current_user
from crud.user import userCrud
from models import Users
from schemas.login import Login
from schemas.token import TokenInfo
from schemas.user import UpdateUser
from utils.resp_code import resp_200,resp_500


@oauth_api.post("/login",summary="docs接口文档登录 && 登录接口")
async def login_access_token(
        # form_data: OAuth2PasswordRequestForm = Depends()
        form_data: Login
) :
    """ 兼容OAuth2的令牌登录，为接口文档的请求获取访问令牌 """
    current_user = userCrud.authenticate(form_data.username,form_data.password)
    token_info = TokenInfo.from_orm(current_user)
    token = create_access_token(token_info.dict())
    # 这里'access_token'和'token_type'一定要写,否则get_current_user依赖拿不到token
    # 可添加字段(先修改schemas/token里面的Token返回模型)
    try :
        update_data = UpdateUser(isActive=True,last_active_time=datetime.datetime.now())
        userCrud.update(current_user.name,update_data.dict(exclude_none=True))
    except Exception as e :
        logger.error(f'数据库连接失败！-- {e}')
        return resp_500(msg=f'数据库连接失败！')
    return resp_200(data={"token" : token,"token_type" : "bearer"})
    # return {"access_token": token, "token_type": "bearer"}


@oauth_api.post('/logout')
async def user_logout(user: Users = Depends(get_current_user)) :
    try :
        update_data = UpdateUser(isActive=False,last_active_time=datetime.datetime.now())
        userCrud.update(user.name,update_data.dict(exclude_none=True))
    except Exception as e :
        logger.error(f'数据库连接失败-- {e}')
        return resp_500(msg=f'数据库连接失败!')
    return resp_200(msg="登出成功！")

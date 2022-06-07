"""
author:dlr123
date:2022年05月31日
"""
from datetime import datetime

from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.logger import logger
from core.security import get_current_user,create_access_token
from crud.user import UserCrud,userCrud
from models.user.users import Users
from schemas.token import TokenInfo
from schemas.user import OutputUser
from schemas.user import UserIn,UpdateUser
from utils.custom_exc import UserNotExist
from utils.resp_code import resp_200,resp_500

test_api = APIRouter(tags=['test'])


@test_api.post('/')
async def hello_world(userin: UserIn) :
    usercrud = UserCrud()
    result = usercrud.authenticate(userin.name,'123456')
    if result :
        out_res = TokenInfo.from_orm(result)
        return resp_200(data=out_res.dict())
    else :
        raise UserNotExist(err_desc=f"{userin.name}不存在")


@test_api.get('/user')
async def get_user_info(user: Users = Depends(get_current_user)) :
    return resp_200(data=OutputUser.from_orm(user))


@test_api.post("/login",summary="docs接口文档登录 && 登录接口")
async def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()
) :
    """ 兼容OAuth2的令牌登录，为接口文档的请求获取访问令牌 """
    current_user = userCrud.authenticate(form_data.username,form_data.password)
    token_info = TokenInfo.from_orm(current_user)
    token = create_access_token(token_info.dict())
    # 这里'access_token'和'token_type'一定要写,否则get_current_user依赖拿不到token
    # 可添加字段(先修改schemas/token里面的Token返回模型)
    try :
        update_data = UpdateUser(isActive=True,last_active_time=datetime.now())
        userCrud.update(current_user.name,update_data.dict(exclude_none=True))
    except Exception as e :
        logger.error(f'数据库连接失败！-- {e}')
        return resp_500(msg=f'数据库连接失败！')
    return {"access_token" : token,"token_type" : "bearer"}

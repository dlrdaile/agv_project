"""
author:dlr123
date:2022年06月07日
"""
import datetime

from apis.oauth import oauth_api
from apis.oauth.emails import EmailValidForm
from apis.oauth.emails import valid_email
from core.logger import logger
from core.security import get_password_hash
from crud.user import userCrud
from schemas.user import CreateUser
from utils.resp_code import resp_400,resp_500,resp_200


@oauth_api.post('/register')
async def register_user(userInfo: CreateUser) :
    user_name = userCrud.get_by_name(userInfo.name)
    if user_name != None :
        return resp_400(msg="用户名已经存在，请更换用户名")
    user_email = userCrud.get_by_email(userInfo.email)
    if user_email != None :
        return resp_400(msg="该邮箱已经被注册，请更换邮箱")
    emailvalidData = EmailValidForm(email=userInfo.email,valid_code=userInfo.code)
    await valid_email(emailvalidData)
    try :
        userInfo.hashed_password = get_password_hash(userInfo.password)
        userInfo.address_id = userInfo.address[1]
        userInfo.create_time = datetime.datetime.now()
        userCrud.create(userInfo)
    except Exception as e :
        logger.error(f'数据库连接失败！-- {e}')
        return resp_500(msg=f'数据库连接失败！')
    return resp_200(msg="创建用户成功！")

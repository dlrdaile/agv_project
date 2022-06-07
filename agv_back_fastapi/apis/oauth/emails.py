"""
author:dlr123
date:2022年06月06日
"""
import time
from typing import List
from enum import Enum
from faker import Faker
from fastapi import (
    BackgroundTasks,
    Depends
)
from fastapi_mail import FastMail,MessageSchema,ConnectionConfig
from pydantic import EmailStr,BaseModel
from sqlmodel import select,update
from starlette.responses import JSONResponse

from apis.oauth import oauth_api
from core.logger import logger
from core.security import get_password_hash
from crud.user import userCrud
from db.session import get_session
from models.user.emails import EmailValid
from models.user.users import Users
from utils import resp_500,resp_200,resp_400
from utils.custom_exc import ErrorUser,UserNotExist


class GetCodePath(str,Enum):
    register = "register"
    forget = "forget"

class EmailSchema(BaseModel) :
    email: List[EmailStr]


class EmailValidForm(BaseModel) :
    email: EmailStr
    valid_code: str


fake = Faker()

conf = ConnectionConfig(
    MAIL_USERNAME="965794928@qq.com",
    MAIL_PASSWORD="hfddddxogzuibfed",
    MAIL_FROM="965794928@qq.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.qq.com",
    MAIL_FROM_NAME="dllr",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def valid_email(validData: EmailValidForm) :
    session = get_session()
    email = validData.email
    valid_code = validData.valid_code
    sql = select(EmailValid).where(EmailValid.email == email)
    try :
        result = session.exec(sql).one()
        current_time = time.time()
        if valid_code != result.valid_code :
            raise ErrorUser("验证码错误")
        session.refresh(result)
        session.delete(result)
        session.commit()
        if (current_time - result.valid_time) > result.valid_duration :
            raise ErrorUser("验证码过期了")
    except ErrorUser as e:
        raise ErrorUser(e.err_desc)
    except Exception as e:
        session.rollback()
        raise UserNotExist("邮箱所属用户无验证码信息，请先获得验证码")
    return email


@oauth_api.post("/getcode/{path}")
async def send_in_background(
        background_tasks: BackgroundTasks,
        email: EmailStr,
        path: GetCodePath
) :
    user = userCrud.get_by_email(email)
    if path == GetCodePath.register :
        if user != None :
            return resp_400(msg="该邮箱已经被使用，请更换邮箱")
    else :
        if user == None:
            return resp_400(msg="该邮箱所属用户不存在，请先注册")
    pass_num = fake.pystr(min_chars=6,max_chars=6)
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[email,],
        body=f"email:{email} 的校验码是 {pass_num}",
    )
    session = get_session()
    try :
        sql = update(EmailValid).where(EmailValid.email == email).values({
            "valid_code" : pass_num,
            "valid_time" : time.time()
        })
        result = session.exec(sql)
        if result.rowcount == 0 :
            session.rollback()
            try :
                valid_email = EmailValid(email=email,valid_code=pass_num)
                session.add(valid_email)
                session.commit()
            except :
                session.rollback()
        else :
            session.commit()
    except :
        session.rollback()
    finally :
        session.close()
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message,message)
    return JSONResponse(status_code=200,content={"message" : "email has been sent"})


@oauth_api.post("/forget")
async def send_in_background(*,email: EmailStr = Depends(valid_email),new_password: str) :
    session = get_session()
    try :
        sql = update(Users).where(Users.email == email).values({
            "hashed_password" : get_password_hash(new_password)
        })
        session.exec(sql)
        session.commit()
    except Exception as e :
        session.rollback()
        logger.error(f'数据库连接失败！-- {e}')
        return resp_500(msg=f'数据库连接失败！')
    return resp_200(msg="密码修改成功")

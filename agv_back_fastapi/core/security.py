#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/19 19:49
# @Author : zxiaosi
# @desc : 安全配置 https://fastapi.tiangolo.com/zh/advanced/security/oauth2-scopes/#global-view
from datetime import datetime,timedelta
from typing import Union,Optional

from fastapi import Depends,HTTPException,Header,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from passlib.context import CryptContext

from core import settings
from schemas.token import TokenInfo
from utils import AccessTokenFail

ALGORITHM = "HS256"  # 加密算法
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")  # 加密密码
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/test/login")


def get_password_hash(password: str) -> str :
    """ 加密明文密码 """
    return pwd_context.hash(password)


def verify_password(password: str,hashed_password: str) -> bool :
    """ 验证明文密码 与 加密后的密码 是否一致 """
    return pwd_context.verify(password,hashed_password)


def create_access_token(data: dict,expires_delta: Optional[timedelta] = None) -> str :
    """
    生成token
    :param data: 存储数据
    :param expires_delta: 有效时间
    :return: 加密后的token
    """
    to_encode = data.copy()
    if expires_delta :
        expire = datetime.utcnow() + expires_delta
    else :
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})  # eg: {'sub': '1', scopes: ['items'] 'exp': '123'}
    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


# https://www.cnblogs.com/CharmCode/p/14191112.html?ivk_sa=1024320u
async def check_jwt_token(token: Optional[str] = Header(...)) -> Union[str,TokenInfo] :
    """ 解密token """
    try :
        payload = jwt.decode(token=token,key=settings.SECRET_KEY,algorithms=[ALGORITHM])
        return TokenInfo(**payload)
    except Exception as e :  # jwt.JWTError, jwt.ExpiredSignatureError, AttributeError
        raise AccessTokenFail(f'token已过期! -- {e}')


async def get_current_user(token: str = Depends(oauth2_scheme)) :
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"},
    )
    try :
        tokeninfo: TokenInfo = await check_jwt_token(token)
        username: str = tokeninfo.name
        id = tokeninfo.id
        if username is None :
            raise credentials_exception
    except JWTError :
        raise credentials_exception
    from crud.user import userCrud
    user = userCrud.get(id)
    if user is None :
        raise credentials_exception
    userCrud.update(user.name,{'last_active_time' : datetime.now()})
    return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

if __name__ == '__main__' :
    # 对 '123456' 加密后得到的值不相同
    print(get_password_hash('123456'))

    # 但 加密前 和 加密后 验证是一致的
    print(verify_password('123456','$2b$12$I5lfn4eO8M0oH4yYQWjSQ.t4VJz9cGKXA.ht6syIG6tAXmbnQywqa'))  # True
    print(verify_password('123456','$2b$12$h58wHhABGgNSRfQCqYFod.0mycfuLZIWQmtvKgP9s0VyYs78In6b.'))  # True

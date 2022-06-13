"""
author:dlr123
date:2022年05月31日
"""
from datetime import datetime
from typing import Optional,List

from pydantic import Field,EmailStr
from sqlmodel import SQLModel


class UserIn(SQLModel) :
    """ 共享模型字段 """
    name: str = Field(...,max_length=10,min_length=3)


class UpdateUser(SQLModel) :
    hashed_password: Optional[str] = Field(default=None,description="用户hash密码")
    email: Optional[EmailStr] = Field(default=None,description="用户邮箱")
    isActive: Optional[bool] = None
    last_active_time: Optional[datetime] = None
    phone: Optional[int] = Field(default=None)
    nickname: Optional[str] = None
    address_id: Optional[int] = None


class CreateUser(UpdateUser,UserIn) :
    password: str
    isActive: bool = False
    nickname: str
    address: List[int]
    email: EmailStr
    create_time: datetime = datetime.now()
    isAdmin: bool = False
    code: str = Field(max_length=6)


class OutputUser(UserIn) :
    email: Optional[EmailStr] = Field(default=None,description="用户邮箱")
    roles: Optional[List[str]] = None
    phone: Optional[int] = Field(default=None)
    address_id: Optional[int] = None
    nickname: str
    create_time: datetime

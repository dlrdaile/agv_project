"""
author:dlr123
date:2022年05月31日
"""
from typing import Optional
from sqlmodel import SQLModel
from pydantic import BaseModel,Field,EmailStr


class UserIn(SQLModel) :
    """ 共享模型字段 """
    name: str = Field(...,max_length=10,min_length=3)


class UpdateUser(UserIn):
    password: str = Field(...,max_length=16,min_length=6)
    email: Optional[EmailStr] = Field(default=None,description="用户邮箱")


class CreateUser(UpdateUser) :
    id: Optional[int] = Field(default=None)
    isAdmin: bool = Field(default=False)

class OutputUser(UserIn):
    email: Optional[EmailStr] = Field(default=None,description="用户邮箱")
    isAdmin: bool = Field(default=False)

"""
author:dlr123
date:2022年05月31日
"""
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel,Field,Column,String


class User(SQLModel,table=True) :
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(index=True,nullable=False,description="用户名",
                      schema_extra={"comment" : "用户名","unique" : True})
    hashed_password: str
    email: Optional[EmailStr] = Field(default=None,description="用户邮箱")
    phone:Optional[int] = Field(default=None)
    isAdmin: bool = Field(default=False)


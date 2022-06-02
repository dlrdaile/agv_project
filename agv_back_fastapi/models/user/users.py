"""
author:dlr123
date:2022年05月31日
"""
from datetime import datetime
from typing import Optional,List

from pydantic import EmailStr
from sqlmodel import SQLModel,Field,Relationship


class Users(SQLModel,table=True) :
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(index=True,nullable=False,description="用户名",
                      schema_extra={"comment" : "用户名","unique" : True})
    hashed_password: str
    # 用户状态
    isActiveL: bool = False
    create_time: datetime = datetime.now()
    last_active_time: Optional[datetime] = None
    # 用户信息
    isAdmin: bool = Field(default=False)
    nickname: str = Field(min_length=3,max_length=20)
    email: Optional[EmailStr] = Field(default=None,description="用户邮箱")
    phone: Optional[int] = Field(default=None)

    address_id: Optional[int] = Field(default=None,foreign_key="city.id")
    address: Optional["City"] = Relationship(back_populates="users")

    userItems: List["UserItems"] = Relationship(back_populates="user")

"""
author:dlr123
date:2022年06月02日
"""
from typing import Optional,List

from sqlmodel import SQLModel,Field,Relationship


class Provincial(SQLModel,table=True) :
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(index=True,min_length=3,max_length=50)
    cities: list["City"] = Relationship(back_populates="province")
    pass


class City(SQLModel,table=True) :
    union_id:Optional[int] = Field(default=None,primary_key=True)
    id: Optional[int] = Field(default=None)
    name: str = Field(min_length=3,max_length=50)
    province_id: Optional[int] = Field(default=None,foreign_key="provincial.id")
    province: Optional[Provincial] = Relationship(back_populates="cities")
    userList:List["Users"] = Relationship(back_populates="address")

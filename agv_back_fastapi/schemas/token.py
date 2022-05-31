#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/12/24 14:48
# @Author : zxiaosi
# @desc : token
from typing import Optional
from schemas.user import UserIn
from pydantic import Field
from sqlmodel import SQLModel


class Token(SQLModel):
    """ token """
    access_token: str
    token_type: str


class TokenInfo(UserIn):
    """ token返回的user模型 """
    id: Optional[int] = Field(default=None)
    isAdmin: bool = Field(default=False)


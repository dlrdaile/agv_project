#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 17:27
# @Author : zxiaosi
# @desc : 数据库会话
# https://www.osgeo.cn/sqlalchemy/orm/extensions/asyncio.html?highlight=async#asynchronous-i-o-asyncio
from sqlmodel import create_engine,Session

from core import settings

# 创建表引擎
engine = create_engine(
    url=settings.DATABASE_URI,  # 数据库uri
    echo=settings.DATABASE_ECHO,  # 是否打印日志
    # pool_size=10,  # 队列池个数
    # max_overflow=20,  # 队列池最大溢出个数
)
def get_session_context():
    with Session(engine) as session:
        yield session

def get_session():
    return Session(engine)
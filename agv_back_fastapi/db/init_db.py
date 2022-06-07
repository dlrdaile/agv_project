#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/25 22:08
# @Author : zxiaosi
# @desc : 创建与删除所有表, 初始化数据
from sqlmodel import SQLModel,Session,select
from crud.user import userCrud
from core.logger import logger
from core import get_password_hash
from db import engine
from models import *


def init_db(isdrop=False) :
    """ 创建 models/__init__ 下的所有表 """
    try :
        if isdrop:
            drop_db()  # 删除所有的表
        SQLModel.metadata.create_all(engine)  # 创建数据库
        logger.info("创建表成功!!!")
    except Exception as e :
        logger.error(f"创建表失败!!! -- 错误信息如下:\n{e}")
    finally :
        engine.dispose()
        return engine


def drop_db() :
    """ 删除 models/__init__ 下的所有表 """
    try :
        SQLModel.metadata.drop_all(engine)
        logger.info("删除表成功!!!")
    except Exception as e :
        logger.error(f"删除表失败!!! -- 错误信息如下:\n{e}")
    finally :
        engine.dispose()


# def excute_sql():
#     with Session(engine) as session:
#         session.exec()

def init_data() :
    """ 初始化表数据 """
    with Session(engine) as session :
        try :
            user = userCrud.get_by_name('admin')
            if user is None :
                admin = Users(name="admin",
                              hashed_password=get_password_hash("123456"),
                              email="965794928@qq.com",
                              nickname = "小甜甜",
                              isAdmin=True
                              )
                session.add(admin)
                session.commit()
                logger.info(f"成功初始化表数据!!!")
        except Exception as e :
            session.rollback()
            logger.error(f"初始化表数据失败!!! -- 错误信息如下:\n{e}")


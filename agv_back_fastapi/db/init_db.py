#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/25 22:08
# @Author : zxiaosi
# @desc : 创建与删除所有表, 初始化数据
from sqlmodel import SQLModel
from core.logger import logger
from db import engine


def init_db(isdrop=False) :
    """ 创建 models/__init__ 下的所有表 """
    try :
        if isdrop :
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

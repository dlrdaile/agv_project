"""
author:dlr123
date:2022年06月30日
"""
from models.user.users import Users
from fastapi import FastAPI
from db.session import get_session
from sqlmodel import not_,and_
from datetime import datetime,timedelta
from core.logger import logger
from apscheduler.schedulers.background import BackgroundScheduler


def detectUserStatus() :
    with get_session() as session :
        time_delta = timedelta(hours=2)
        critical_datetime = datetime.now() - time_delta
        try :
            result = session.query(Users). \
                filter(and_(not_(Users.isAdmin),
                            Users.last_active_time <= critical_datetime,Users.isActive)). \
                update({'isActive' : False}
                       ,synchronize_session=False)
            session.commit()
            logger.info(f"共有{result}个用户状态被修改")
        except Exception as e :
            session.rollback()
            logger.error(f"用户状态信息消除失败,因为:{e}")


def register_timer(app: FastAPI) :
    sche = BackgroundScheduler()
    sche.add_job(detectUserStatus,next_run_time=datetime.now(),trigger='interval',hours=2,id="detectUserStatus")
    app.state.sche = sche
    sche.start()

"""
author:dlr123
date:2022年06月30日
"""
from models.user.users import Users
from models.item.items import UserOrder,OrderStatus
from models.car.tasks import Tasks,TaskStatus
from models.item.links import TaskEquipmentLink
from fastapi import FastAPI
from db.session import get_session
from sqlmodel import not_,and_,select,func
from datetime import datetime,timedelta
from core.logger import logger
from apscheduler.schedulers.background import BackgroundScheduler
import random

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


def detectOrderStatus() :
    with get_session() as session :
        try :
            sql = select(UserOrder).where(UserOrder.status == OrderStatus.Processing).where(
                UserOrder.task_id == None).order_by(UserOrder.create_time)
            order = session.exec(sql).first()
            if order is not None :
                task = Tasks(
                    description = order.task_description,
                    create_time = datetime.now()
                )
                task_equipment_link_list = []
                for process_link in order.item.process_links:
                    task_equipment_link = TaskEquipmentLink(order = process_link.order)
                    # 设备分配算法在这里实现
                    equiment = random.choice(process_link.process.equipment)
                    task_equipment_link.equipment = equiment
                    task_equipment_link.task = task
                    task_equipment_link_list.append(task_equipment_link)
                order.task = task
                order.start_time = task.create_time
                session.add(task)
                session.add(order)
                session.add_all(task_equipment_link_list)
                session.commit()
                session.refresh(task)
                logger.info(f"第{order.id}号订单任务分配成功,分配后的任务编号为{task.id}")
        except Exception as e :
            session.rollback()
            logger.error(f"订单调度失败,因为:{e}")


def register_timer(app: FastAPI) :
    sche = BackgroundScheduler()
    sche.add_job(detectUserStatus,next_run_time=datetime.now(),trigger='interval',hours=2,id="detectUserStatus")
    sche.add_job(detectOrderStatus,next_run_time=datetime.now(),trigger='interval',seconds=3,id="detectOrderStatus")
    app.state.sche = sche
    sche.start()

import datetime
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request, UploadFile, Depends

from core.config import settings
from core.logger import logger
from core.security import get_current_user
from crud.items import itemCrud
from db.session import get_session
from models.car.tasks import Tasks, TaskStatus
from models.item.items import Items
from models.item.links import ItemProcessLink
from models.item.items import UserOrder, OrderStatus
from models.user.users import Users
from schemas.items import QueryInItems, OutputItems, SearchItems
from utils.resp_code import resp_200, resp_500, resp_400
from models.car.car import Cars, CarStatus
from enum import Enum
from core import FastAPiNode


class CtrOption(int, Enum):
    ACTIVATE = 0
    PAUSE = 1
    CONTINUE = 2
    CANCEL = 3
    INACTIVATE = 4


car_api = APIRouter(prefix='/cars')


@car_api.post('/setStatus')
async def setStatus(car_id: int, ctl_code: int, req: Request, user: Users = Depends(get_current_user)):
    res = resp_200(msg="success")
    with get_session() as session:
        try:
            car: Cars = session.query(Cars).get(car_id)
            if car is None:
                raise ValueError("the car is not exit")
            if ctl_code == CtrOption.PAUSE:
                if car.status == CarStatus.WORKING:
                    req.state.rosnode.cancelGoal()
                    # car.status = CarStatus.PAUSE
                    # session.add(car)
                else:
                    logger.warning("the car is not pausing,it can't")
                    res = resp_400(msg="the car has been pausing!")
            elif ctl_code == CtrOption.CONTINUE:
                if car.status == CarStatus.PAUSE:
                    car.status = CarStatus.FREE
                    session.add(car)
                elif car.status == CarStatus.FREE:
                    res = resp_400(msg="the car is free,not need to set to continue")
                else:
                    res = resp_400(msg="the car can not be set to continue")
            elif ctl_code == CtrOption.ACTIVATE:
                if car.status == CarStatus.INACTIVATE:
                    if car.current_task_id is not None:
                        task = session.query(Tasks).get(car.current_task_id)
                        if task is not None:
                            car.status = CarStatus.PAUSE
                        else:
                            car.current_task_id = None
                            car.status = CarStatus.FREE
                    else:
                        car.status = CarStatus.FREE
                    session.add(car)
                else:
                    res = resp_400(msg="the car can has been activated")
            elif ctl_code == CtrOption.INACTIVATE:
                if car.status == CarStatus.WORKING:
                    res = resp_400(msg="please pause the car firstly or wait for it complete")
                elif car.status == CarStatus.INACTIVATE:
                    res = resp_400(msg="the car is inactivate,it is not need to set")
                else:
                    car.status = CarStatus.INACTIVATE
                session.add(car)
            else:  # cancel the task
                if car.status == CarStatus.PAUSE and car.current_task_id is not None:
                    task: Tasks = session.query(Tasks).get(car.current_task_id)
                    if task is not None:
                        task.end_time = datetime.datetime.now()
                        task.status = TaskStatus.FAIL
                        try:
                            order: UserOrder = task.UserOrder[0]
                        except:
                            order: UserOrder = task.UserOrder
                        order.status = OrderStatus.Fail
                        task.fail_reason = "we can not complete the order"
                        order.reject_or_fail_reason = "we can not complete the order"
                    car.status = CarStatus.FREE
                    car.current_task_id = None
                    session.add(task)
                    session.add(car)
                    session.add(order)
                elif car.status == CarStatus.WORKING:
                    res = resp_400(msg="please pause the car firstly")
                else:
                    res = resp_400(msg='the car can not be cancel')
            session.commit()
        except Exception as e:
            session.rollback()
            logger.warning(f"ros status control error! because: {e}")
            res = resp_400(msg="set car status fail")
    return res


@car_api.post('/runDemo')
async def setStatus(taskId: int, req: Request, car_id: int = 1,
                    user: Users = Depends(get_current_user)):
    res = resp_200(msg="success")
    with get_session() as session:
        try:
            car: Cars = session.query(Cars).get(car_id)
            if car is None:
                raise ValueError("the car is not exit")
            if car.status != CarStatus.FREE:
                if car.status == CarStatus.WORKING:
                    if taskId == 0:
                        req.state.rosnode.cancelDemoGoal()
                    else:
                        res = resp_400(msg="the car can not excecute the demo now!")
                else:
                    res = resp_400(msg="the car can not excecute the demo now!")
            else:
                car.status = CarStatus.WORKING
                session.add(car)
                session.commit()
                started = req.state.rosnode.callDemo(taskId)
                if not started:
                   res = resp_400(msg="the server is not start!")
        except Exception as e:
            session.rollback()
            logger.warning(f"demo run error! because: {e}")
            res = resp_400(msg="demo run fail")
    return res

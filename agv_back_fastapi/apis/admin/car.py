import datetime
import uuid
from pathlib import Path

from fastapi import APIRouter,Request,UploadFile,Depends

from core.config import settings
from core.logger import logger
from core.security import get_current_user
from crud.items import itemCrud
from db.session import get_session
from models.car.tasks import Tasks,TaskStatus
from models.item.items import Items
from models.item.links import ItemProcessLink
from models.item.items import UserOrder,OrderStatus
from models.user.users import Users
from schemas.items import QueryInItems,OutputItems,SearchItems
from utils.resp_code import resp_200,resp_500,resp_400
from models.car.car import Cars,CarStatus
from core.rosClass import rosNode
from enum import Enum
class CtrOption(int,Enum):
    PAUSE = 0
    CONTINUE = 1
    CANCEL = 2

car_api = APIRouter(prefix='/car')

car_api.post('/setStatus')
async def setStatus(car_id:int,ctl_code:CtrOption,user: Users = Depends(get_current_user)):
    res = resp_200(msg="success")
    with get_session() as session:
        try:
            car:Cars = session.query(Cars).get(car_id)
            if car is None:
                raise ValueError("the car is not exit")
            if ctl_code == CtrOption.PAUSE:
                if car.status == CarStatus.WORKING:
                    rosNode.cancelGoal()
                elif car.status == CarStatus.FREE:
                    car.status = CarStatus.PAUSE
                    session.add(car)
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
                    pass
            else:
                if car.status == CarStatus.PAUSE and car.current_task_id is not None:
                    task:Tasks = session.query(Tasks).get(car.current_task_id)
                    if task is not None:
                        task.end_time = datetime.datetime.now()
                        task.status = TaskStatus.FAIL
                        try:
                            order:UserOrder = task.UserOrder[0]
                        except:
                            order:UserOrder = task.UserOrder
                        order.status = OrderStatus.Fail
                        task.fail_reason = "we can not complete the order"
                        order.reject_or_fail_reason = "we can not complete the order"
                    car.status = CarStatus.FREE
                    car.current_task_id = None
                    session.add(task)
                    session.add(car)
                    session.add(order)
                    pass
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
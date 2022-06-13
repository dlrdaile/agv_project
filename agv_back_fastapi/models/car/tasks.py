"""
author:dlr123
date:2022年06月02日
"""
from datetime import datetime
from enum import Enum
from typing import Optional,List

from sqlmodel import SQLModel,Field,Relationship

# from models.item.links import TaskEquipmentLink


class TaskStatus(int,Enum) :
    WAITING = 0
    ACTIVE = 1
    SUCCEEDED = 2
    FAIL = 3


class Tasks(SQLModel,table=True) :
    """
        任务序列
    """
    id: Optional[int] = Field(default=None,primary_key=True)
    status: TaskStatus = TaskStatus.WAITING
    start_time: datetime = datetime.now()
    end_time: Optional[datetime] = None
    UserOrders: Optional["UserOrder"] = Relationship(back_populates="task")
    equipment_links: List["TaskEquipmentLink"] = Relationship(back_populates="task")

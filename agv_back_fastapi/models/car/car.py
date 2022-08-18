"""
author:dlr123
date:2022年07月06日
"""
from enum import Enum
from typing import Optional,List

from sqlmodel import SQLModel,Field,Relationship


class CarStatus(int,Enum) :
    INACTIVATE = 0  # 关机或者ros系统没有开启时表示为关机状态
    FREE = 1  # ros系统开启时，但没有分配任务，表示为空闲状态
    WORKING = 2  # 当小车在执行任务时，表示为工作状态
    PAUSE = 3
    CHARGING = 4  # 当小车处于充电状态时
    Fault = 5  # 当小车异常时，表示为故障状态


class Cars(SQLModel,table=True) :
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str
    productor: Optional[str] = None
    isSimulation: bool = True
    fault_reason: Optional[str] = None
    description: Optional[str] = None
    status: CarStatus = CarStatus.INACTIVATE
    current_task_id: Optional[int] = None
    ip: str
    port: str
    weight: float
    tasks: List["Tasks"] = Relationship(back_populates="car")
    devices: List["DeviceTypeLink"] = Relationship(back_populates="car_link")

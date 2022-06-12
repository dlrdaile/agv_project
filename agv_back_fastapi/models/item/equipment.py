"""
author:dlr123
date:2022年06月02日
"""
from enum import Enum
from typing import Optional,List

from sqlmodel import Field,Relationship

from models.item.links import ProcessEquipmentLink,TaskEquipmentLink
from schemas.position import DevicePositon


class EquipmentStatus(int,Enum) :
    Free = 0  # 空闲
    Occupy = 1  # 占用
    Damage = 2  # 损坏


class Equipment(DevicePositon,table=True) :
    """
        定义加工设备的设备信息
        设备和工序间为多对多的关系
    """
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    equipStatus: EquipmentStatus = 0
    process: List["Process"] = Relationship(back_populates="equipment",link_model=ProcessEquipmentLink)
    tasks_links: List[TaskEquipmentLink] = Relationship(back_populates="equipment")

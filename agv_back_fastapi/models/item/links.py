"""
author:dlr123
date:2022年06月02日
"""
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel,Field,Relationship


class SubTaskStatus(int,Enum) :
    WAITING = 0
    ACTIVE = 1
    SUCCEEDED = 2
    FAIL = 3
    PAUSE = 4


class ItemProcessLink(SQLModel,table=True) :
    item_id: Optional[int] = Field(
        default=None,foreign_key="items.id",primary_key=True
    )
    process_id: Optional[int] = Field(
        default=None,foreign_key="process.id",primary_key=True
    )
    order: int = Field(default=None,primary_key=True)
    item: Optional["Items"] = Relationship(back_populates="process_links")
    process: Optional["Process"] = Relationship(back_populates="item_links")


class ProcessEquipmentLink(SQLModel,table=True) :
    process_id: Optional[int] = Field(
        default=None,foreign_key="process.id",primary_key=True
    )
    equipment_id: Optional[int] = Field(
        default=None,foreign_key="equipment.id",primary_key=True
    )


class TaskEquipmentLink(SQLModel,table=True) :
    task_id: Optional[int] = Field(
        default=None,foreign_key="tasks.id",primary_key=True
    )
    equipment_id: Optional[int] = Field(
        default=None,foreign_key="equipment.id",primary_key=True
    )
    order: int = Field(default=None,primary_key=True)
    status:SubTaskStatus = SubTaskStatus.WAITING
    current_task_iswork:bool = False
    task: Optional["Tasks"] = Relationship(back_populates="equipment_links")
    equipment: Optional["Equipment"] = Relationship(back_populates="tasks_links")

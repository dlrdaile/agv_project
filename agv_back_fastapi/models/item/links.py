"""
author:dlr123
date:2022年06月02日
"""
from typing import Optional,List

from sqlmodel import SQLModel,Field,Relationship


class ItemProcessLink(SQLModel,table=True) :
    item_id: Optional[int] = Field(
        default=None,foreign_key="items.id",primary_key=True
    )
    process_id: Optional[int] = Field(
        default=None,foreign_key="process.id",primary_key=True
    )
    order: int = Field(default=None,primary_key=True)
    item: "Items" = Relationship(back_populates="process_links")
    process: "Process" = Relationship(back_populates="item_links")


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
    order: int
    task: "Tasks" = Relationship(back_populates="equipment_links")
    equipment: "Equipment" = Relationship(back_populates="tasks_links")

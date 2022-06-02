"""
author:dlr123
date:2022年06月02日
"""
from typing import Optional,List

from sqlmodel import SQLModel,Field,Relationship

from models.item.links import ItemProcessLink,ProcessEquipmentLink


class Process(SQLModel,table=True) :
    """
        定义加工工艺
        其中工艺和设备间都是多对多的关系
    """
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(index=True,max_length=10)
    description: Optional[str] = None
    item_links: List[ItemProcessLink] = Relationship(back_populates="process")
    equipment: List["Equipment"] = Relationship(back_populates="process",link_model=ProcessEquipmentLink)

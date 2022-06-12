"""
author:dlr123
date:2022年06月02日
"""
from datetime import datetime
from enum import Enum
from typing import Optional,List

from sqlmodel import SQLModel,Field,Relationship

from models.car.tasks import Tasks
from models.item.links import ItemProcessLink
from models.user.users import Users


class ItemStatus(int,Enum) :
    NotProcessed = 0
    Processing = 1
    Reject = 2
    Finished = 3
    Fail = 4


class Items(SQLModel,table=True) :
    """
        定义了系统预定义的一些商品
        该商品与工序之间为多对多的关系
    """
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(index=True,max_length=10)
    description: Optional[str] = None
    image_path: Optional[str] = None

    isPublic: bool = True
    Provider: str = 'admin'

    price: float
    weight: float

    userItems: List["UserItems"] = Relationship(back_populates="item")
    process_links: List[ItemProcessLink] = Relationship(back_populates="item")


class UserItems(SQLModel,table=True) :
    """
        定义了用户和订单的一对多关系
    """
    id: Optional[int] = Field(default=None,primary_key=True)
    status: ItemStatus = 0
    create_time: datetime = Field(default=datetime.now())  # 表单提交时间
    start_time: Optional[datetime] = Field(default=None)  # 表单开始调度时间
    end_time: Optional[datetime] = Field(default=None)  # 表单结束时间
    description: Optional[str] = None  # 对该订单进行描述
    user_id: Optional[int] = Field(default=None,foreign_key="users.id")
    item_id: Optional[int] = Field(default=None,foreign_key="items.id")
    task_id: Optional[int] = Field(default=None,foreign_key="tasks.id")
    item: Optional[Items] = Relationship(back_populates="userItems")
    user: Optional[Users] = Relationship(back_populates="userItems")
    task: Optional[Tasks] = Relationship(back_populates="userItems")

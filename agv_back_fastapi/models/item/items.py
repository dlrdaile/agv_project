"""
author:dlr123
date:2022年06月02日
"""
from datetime import datetime
from enum import Enum
from typing import Optional,List
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import SQLModel,Field,Relationship

from models.car.tasks import Tasks
from models.item.links import ItemProcessLink
from models.user.users import Users


class OrderStatus(int,Enum) :
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
    create_time: datetime = Field(default=datetime.now())  # 商品创建时间
    isPublic: bool = True
    Provider: str = 'admin'
    IsShowToClient: bool = True
    price: float
    weight: float
    user_id: Optional[int] = Field(default=None,foreign_key="users.id")
    user: Optional[Users] = Relationship(back_populates="selfItems")
    UserOrders: List["UserOrder"] = Relationship(back_populates="item",
                                                 sa_relationship_kwargs=dict(cascade="save-update, merge, "
                                                                                     "delete, delete-orphan"))
    process_links: List[ItemProcessLink] = Relationship(back_populates="item",
                                                        sa_relationship_kwargs=dict(cascade="save-update, merge, "
                                                                                            "delete, delete-orphan"))


class UserOrder(SQLModel,table=True) :
    """
        定义了用户和订单的一对多关系
    """
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str
    status: OrderStatus = 0
    isEditing: bool = True
    create_time: datetime = Field(default=datetime.now())  # 表单提交时间
    start_time: Optional[datetime] = Field(default=None)  # 表单开始调度时间
    end_time: Optional[datetime] = Field(default=None)  # 表单结束时间
    description: Optional[str] = None  # 对该订单进行描述
    task_description: Optional[str] = None  # 对该订单进行描述
    reject_or_fail_reason: Optional[str] = None
    IsShowToClient: bool = True
    user_id: Optional[int] = Field(default=None,foreign_key="users.id")
    item_id: Optional[int] = Field(default=None,foreign_key="items.id")
    task_id: Optional[int] = Field(default=None,foreign_key="tasks.id")
    item: Optional[Items] = Relationship(back_populates="UserOrders")
    user: Optional[Users] = Relationship(back_populates="UserOrders")
    task: Optional[Tasks] = Relationship(back_populates="UserOrder")

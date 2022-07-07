"""
author:dlr123
date:2022年06月14日
"""
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

from models import OrderStatus


class BaseOrder(SQLModel) :
    id: int
    name: Optional[str] = None
    pass


class QueryOrder(SQLModel) :
    page:int = 1
    limit:int = 10
    desc: Optional[bool] = False
    timeDesc: Optional[bool] = False
    item_id: Optional[list[int]] = None
    editState: Optional[list[bool]] = None
    orderState: Optional[list[OrderStatus]] = None
    IsShowToClient: Optional[list[bool]] = None
    user_id: Optional[list[int]] = None


class UpdateOrder(SQLModel) :
    id:int
    name: Optional[str] = None
    isEditing: Optional[bool] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    description: Optional[str] = None
    task_description: Optional[str] = None  # 对该订单进行描述
    reject_or_fail_reason: Optional[str] = None
    IsShowToClient: Optional[bool] = None
    task_id: Optional[int] = None
    item_id: Optional[int] = None
    status: Optional[OrderStatus] = None

class CreateOrder(SQLModel) :
    name: str
    create_time: datetime
    description: str
    user_id: int
    item_id: int


class DeleteOrder(SQLModel) :
    id: int


class OutputOrder(SQLModel) :
    id: int
    name: str
    create_time: datetime
    description: str
    isEditing: bool
    status: OrderStatus
    item_id: Optional[int]
    IsShowToClient:bool
    user_id: int
    item_name: Optional[str] = None
    reject_or_fail_reason: Optional[str] = None
    task_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

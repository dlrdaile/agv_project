"""
author:dlr123
date:2022年06月12日
"""
from typing import Optional

from sqlmodel import SQLModel


class BaseItem(SQLModel) :
    pass


class CreateItem(SQLModel) :
    name: str
    description: Optional[str] = None
    isPublic: bool = True
    Provider: str = 'admin'
    price: float
    weight: float
    # goods_processes:list[]


class UpdateItem(SQLModel) :
    pass


class DeleteItem(SQLModel) :
    pass


class OutputItems(SQLModel) :
    pass

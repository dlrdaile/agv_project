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
    image_path: Optional[str] = None
    isPublic: bool
    Provider: str
    price: float
    weight: float
    user_id: int

class UpdateItem(SQLModel) :

    name:Optional[str] = None
    description: Optional[str] = None
    isPublic: Optional[bool] = None
    Provider: Optional[str] = None
    price: Optional[float] = None
    weight: Optional[float] = None
    image_path: Optional[str] = None


class OutputItems(SQLModel) :
    id:int
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None
    isPublic: bool
    Provider: str
    price: float
    weight: float

class QueryInItems(SQLModel):
    query :str
    pagenum: int
    pagesize:int

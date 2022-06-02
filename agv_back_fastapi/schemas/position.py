"""
author:dlr123
date:2022年06月02日
"""
from sqlmodel import SQLModel


class Position(SQLModel) :
    x: float
    y: float


class Orientation(SQLModel) :
    x: float = 0
    y: float = 0
    w: float = 0
    z: float


class DevicePositon(Position,Orientation) :
    floor: int

"""
author:dlr123
date:2022年06月02日
"""
from sqlmodel import SQLModel


class Position(SQLModel) :
    x: float
    y: float


class Orientation(SQLModel) :
    yaw:float


class DevicePositon(Position,Orientation) :
    floor: int

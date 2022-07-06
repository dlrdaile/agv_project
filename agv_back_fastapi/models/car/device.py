"""
author:dlr123
date:2022年07月06日
"""
from datetime import datetime
from enum import Enum
from typing import Optional,List
from sqlmodel import SQLModel,Field,JSON,Relationship


class DeviceStatus(int,Enum) :
    INACTIVATE = 0
    ACTIVATE = 1
    FAULT = 2


class BaseDeviceInfo(SQLModel) :
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str
    manufacturer: Optional[str] = None
    status: DeviceStatus = DeviceStatus.INACTIVATE
    fault_reason: Optional[str] = None
    description: Optional[str] = None
    topicName: Optional[str] = None
    topicType: Optional[str] = None


class Battery(BaseDeviceInfo,table=True) :
    currentBattery: float = 12
    maxBattery: float = 12
    minBattery: float = 9.5
    device: Optional["DeviceTypeLink"] = Relationship(back_populates="battery_link")


class Laser(BaseDeviceInfo,table=True) :
    device: Optional["DeviceTypeLink"] = Relationship(back_populates="laser_link")

class Press(BaseDeviceInfo,table=True):
    currentPress: float = 0
    maxPress: float = 5
    device: Optional["DeviceTypeLink"] = Relationship(back_populates="press_link")


class Odom(BaseDeviceInfo,table=True) :
    device: Optional["DeviceTypeLink"] = Relationship(back_populates="odom_link")


class Imu(BaseDeviceInfo,table=True) :
    device: Optional["DeviceTypeLink"] = Relationship(back_populates="imu_link")


class Camera(BaseDeviceInfo,table=True) :
    device: Optional["DeviceTypeLink"] = Relationship(back_populates="camera_link")


class DeviceType(SQLModel,table=True) :
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str
    description: Optional[str] = None


class DeviceTypeLink(SQLModel,table=True) :
    id: Optional[int] = Field(default=None,primary_key=True)
    type_id: Optional[int] = Field(default=None,foreign_key="devicetype.id")
    odom_id: Optional[int] = Field(default=None,foreign_key="odom.id")
    laser_id: Optional[int] = Field(default=None,foreign_key="laser.id")
    camera_id: Optional[int] = Field(default=None,foreign_key="camera.id")
    imu_id: Optional[int] = Field(default=None,foreign_key="imu.id")
    battery_id: Optional[int] = Field(default=None,foreign_key="battery.id")
    press_id: Optional[int] = Field(default=None,foreign_key="press.id")
    car_id: Optional[int] = Field(default=None,foreign_key="cars.id")
    odom_link: Optional[Odom] = Relationship(back_populates="device")
    laser_link: Optional[Laser] = Relationship(back_populates="device")
    camera_link: Optional[Camera] = Relationship(back_populates="device")
    imu_link: Optional[Imu] = Relationship(back_populates="device")
    battery_link: Optional[Battery] = Relationship(back_populates="device")
    press_link: Optional[Press] = Relationship(back_populates="device")
    car_link: Optional["Cars"] = Relationship(back_populates="devices")
    device_datas: List["DeviceData"] = Relationship(back_populates="device")


class DeviceData(SQLModel,table=True) :
    id: Optional[int] = Field(default=None,primary_key=True)
    device_id: Optional[int] = Field(default=None,foreign_key="devicetypelink.id")
    device: Optional[DeviceTypeLink] = Relationship(back_populates="device_datas")
    time: datetime

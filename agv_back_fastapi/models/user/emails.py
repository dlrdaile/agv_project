"""
author:dlr123
date:2022年06月06日
"""
import time
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel,Field


class EmailValid(SQLModel,table=True) :
    id: Optional[int] = Field(default=None,primary_key=True)
    email: EmailStr = Field(index=True)
    valid_code: str = Field(max_length=6,min_length=6)
    valid_time: float = time.time()
    valid_duration: int = 300

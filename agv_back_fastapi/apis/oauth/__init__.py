"""
author:dlr123
date:2022年06月07日
"""
from fastapi import APIRouter

oauth_api = APIRouter(prefix='/oauth')

from .login import *
from .emails import *
from .register import *
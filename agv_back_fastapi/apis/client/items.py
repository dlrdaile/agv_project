"""
author:dlr123
date:2022年06月12日
"""
from fastapi import APIRouter

items_api = APIRouter(prefix='/items')

@items_api.post('/add')
def add_item():
    pass

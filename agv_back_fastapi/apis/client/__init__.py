"""
author:dlr123
date:2022年05月31日
"""
from fastapi import APIRouter

client_api = APIRouter(prefix='/client')
from .items import items_api
from .orders import order_api

client_api.include_router(items_api,tags=['Items'])
client_api.include_router(order_api,tags=['Orders'])

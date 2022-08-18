"""
author:dlr123
date:2022年05月31日
"""
from fastapi import APIRouter

admin_api = APIRouter(prefix='/admin')
from .items import items_api
from .orders import order_api
from .users import user_api
from .car import car_api

admin_api.include_router(items_api,tags=['Items'])
admin_api.include_router(order_api,tags=['Orders'])
admin_api.include_router(user_api,tags=['Users'])
admin_api.include_router(car_api,tags=['Cars'])

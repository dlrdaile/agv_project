"""
author:dlr123
date:2022年05月31日
"""
from fastapi import APIRouter

client_api = APIRouter(prefix='/client')
from .items import items_api

client_api.include_router(items_api,tags=['Items'])

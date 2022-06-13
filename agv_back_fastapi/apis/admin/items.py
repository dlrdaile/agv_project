"""
author:dlr123
date:2022年06月13日
"""

from fastapi import APIRouter,Depends

from core.security import get_current_user
from crud.items import itemCrud
from models.user.users import Users
from schemas.items import QueryInItems,OutputItems
from utils.resp_code import resp_200

items_api = APIRouter(prefix='/items')


@items_api.get('/getitems')
async def get_items(*,user: Users = Depends(get_current_user),query_data: QueryInItems) :
    items = itemCrud.get_multi(query_data.query,user,pageIndex=query_data.pagenum,pageSize=query_data.pagesize)
    output_items = [OutputItems.from_orm(item) for item in items]
    total = itemCrud.get_count(user)
    return resp_200(data=dict(goodslist=output_items,total=total),msg='获得商品数据成功')

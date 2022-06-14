"""
author:dlr123
date:2022年06月13日
"""
import os
from pathlib import Path

from fastapi import APIRouter,Depends

from core.logger import settings,logger
from core.security import get_current_user
from crud.items import itemCrud
from db import get_session
from models import Items
from models.user.users import Users
from schemas.items import QueryInItems,OutputItems
from utils.resp_code import resp_200,resp_400,resp_500

items_api = APIRouter(prefix='/items')


@items_api.get('/getitems')
async def get_items(*,user: Users = Depends(get_current_user),query_data: QueryInItems) :
    items = itemCrud.get_multi(query_data.query,user,pageIndex=query_data.pagenum,pageSize=query_data.pagesize)
    output_items = [OutputItems.from_orm(item) for item in items]
    total = itemCrud.get_count(user)
    return resp_200(data=dict(goodslist=output_items,total=total),msg='获得商品数据成功')

@items_api.delete('/deleteitem')
async def delete_item(*,user: Users = Depends(get_current_user),item_id: int) :
    img_store_dir = Path(settings.PROJECT_ROOT_PATH)
    item = itemCrud.get(item_id)
    img_url = item.image_path
    if settings.BASE_URL in img_url:
        filename = img_url.split('/')[-1]
        img_path = img_store_dir/f'static/img/{filename}'
        os.remove(img_path.absolute())
    if item.user_id != user.id :
        res = resp_400(msg='没有删除该商品的权限')
    else :
        try :
            with get_session() as session:
                try:
                    item = session.query(Items).get(item_id)
                    for procee_item_link in item.process_links:
                        session.delete(procee_item_link)
                    session.commit()
                except Exception as e:
                    logger.error(f'商品删除错误,因为：{e}')
                    return resp_500(msg="数据库操作错误")
            num = itemCrud.remove(item_id)
            if num != 0 :
                res = resp_200(msg="删除成功")
            else :
                res = resp_400(msg="该商品不存在")
        except Exception as e :
            logger.error(f'商品删除错误,因为：{e}')
            res = resp_500(msg="数据库操作错误")
    return res

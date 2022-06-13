"""
author:dlr123
date:2022年06月12日
"""
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter,Request,UploadFile,Depends

from core.config import settings
from core.logger import logger
from core.security import get_current_user
from crud.items import itemCrud
from db.session import get_session
from models.item.items import Items
from models.user.users import Users
from schemas.items import QueryInItems,OutputItems
from utils.resp_code import resp_200,resp_500,resp_400

items_api = APIRouter(prefix='/items')


@items_api.post('/add')
async def add_item(req: Request,file: UploadFile,user: Users = Depends(get_current_user)) :
    form_data = req._form._dict
    items = itemCrud.get_by_name(form_data['name'])
    if items is not None :
        return resp_400(msg="该商品名已经被使用，请更换商品名")
    img_store_dir = Path(settings.PROJECT_ROOT_PATH)
    file_path = Path(file.filename)
    img_uuid = str(uuid.uuid1())
    filename = img_uuid + file_path.suffix
    img_path = img_store_dir/f'static/img/{filename}'
    img_path.write_bytes(file.file.read())
    with get_session() as session :
        try :
            img_store_url = f"{settings.BASE_URL}/static/img/{filename}"
            items = Items(**form_data)
            items.image_path = img_store_url
            items.user_id = user.id
            session.add(items)
            session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'{user.name}添加商品失败,因为：{e}')
            return resp_500(msg='商品添加失败')
        else :
            logger.info(f'{user.name}添加商品成功')
            return resp_200(msg='商品添加成功')


@items_api.post('/getitems')
async def get_items(*,user: Users = Depends(get_current_user),query_data: QueryInItems) :
    try:
        items = itemCrud.get_multi(query_data.query,user,pageIndex=query_data.pagenum,pageSize=query_data.pagesize)
        output_items = [OutputItems.from_orm(item) for item in items]
        total = itemCrud.get_count(user)
    except Exception as e:
        logger.error(f'获取商品列表时数据库查询错误，原因是{e}')
        return resp_500(msg='数据库查询错误')
    return resp_200(data=dict(goodslist=output_items,total=total),msg='获得商品数据成功')

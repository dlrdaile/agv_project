"""
author:dlr123
date:2022年06月12日
"""
import uuid
from pathlib import Path
import os
from fastapi import APIRouter,Request,UploadFile,Depends

from core.config import settings
from core.logger import logger
from core.security import get_current_user
from crud.items import itemCrud
from db.session import get_session
from models.item.items import Items
from models.user.users import Users
from models.item.links import ProcessEquipmentLink,ItemProcessLink
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
    process_queue_ls = form_data['Processes'].split(',')
    with get_session() as session :
        try :
            img_store_url = f"{settings.BASE_URL}/static/img/{filename}"
            items = Items(**form_data)
            items.image_path = img_store_url
            items.user_id = user.id
            item_process_link_ls = []
            for order,process_id in enumerate(process_queue_ls) :
                item_process_link = ItemProcessLink(process_id=process_id,
                                                    order=order)
                items.process_links.append(item_process_link)
                item_process_link_ls.append(item_process_link)
            session.add(items)
            session.add_all(item_process_link_ls)
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
    try :
        items = itemCrud.get_multi(query_data.query,user,pageIndex=query_data.pagenum,pageSize=query_data.pagesize)
        output_items = [OutputItems.from_orm(item) for item in items]
        total = itemCrud.get_count(user,query_data.query)
    except Exception as e :
        logger.error(f'获取商品列表时数据库查询错误，原因是{e}')
        return resp_500(msg='数据库查询错误')
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

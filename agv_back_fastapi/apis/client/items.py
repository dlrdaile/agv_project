"""
author:dlr123
date:2022年06月12日
"""
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter,Request,UploadFile,Depends
from sqlalchemy import or_,and_

from core.config import settings
from core.logger import logger
from core.security import get_current_user
from crud.items import itemCrud
from db.session import get_session
from models.item.items import Items
from models.item.links import ItemProcessLink
from models.user.users import Users
from schemas.items import QueryInItems,OutputItems,SearchItems
from utils.resp_code import resp_200,resp_500,resp_400

items_api = APIRouter(prefix='/items')

async def get_all_items(user: Users = Depends(get_current_user)):
    with get_session() as session:
        try:
            all_items = session.query(Items).filter(and_(Items.IsShowToClient,or_(Items.user_id == user.id,Items.isPublic))).all()
        except Exception as e:
            logger.error(f'获取全部数据失败，原因是{e}')
            return resp_500(msg='数据库查询错误')
        return all_items

@items_api.post('/create')
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
        for output_item in output_items :
            if output_item.Provider == 'admin' :
                output_item.kind = '官方商品'
            elif output_item.user_id == user.id :
                output_item.kind = '自定义商品'
            else :
                output_item.kind = '第三方商品'
        total = itemCrud.get_count(user,query_data.query)
    except Exception as e :
        logger.error(f'获取商品列表时数据库查询错误，原因是{e}')
        return resp_500(msg='数据库查询错误')
    return resp_200(data=dict(goodslist=output_items,total=total),msg='获得商品数据成功')

@items_api.get('/getitems')
async def get_items_for_search(all_items:list[Items] = Depends(get_all_items),user: Users = Depends(get_current_user)):
    kinds = ['官方商品','自定义商品','第三方商品']
    search_items = {kind:[] for kind in kinds}
    for item in all_items :
        search_item = SearchItems.from_orm(item)
        if item.Provider == 'admin' :
            search_items['官方商品'].append(search_item.dict())
        elif item.user_id == user.id :
            search_items['自定义商品'].append(search_item.dict())
        else :
            search_items['第三方商品'].append(search_item.dict())
    return resp_200(data=dict(goodslist=search_items,total=len(all_items)),msg='获得商品数据成功')

@items_api.delete('/delete')
async def delete_item(*,user: Users = Depends(get_current_user),item_id: int) :
    with get_session() as session :
        try :
            item = session.query(Items).get(item_id)
            if item.user_id != user.id :
                res = resp_400(msg='没有删除该商品的权限')
            else :
                item.IsShowToClient = False
                session.add(item)
                session.commit()
                res = resp_200(msg="商品删除成功")
        except Exception as e :
            logger.error(f'商品删除错误,因为：{e}')
            res = resp_500(msg="数据库操作错误")
    return res


@items_api.get('/getitemprocess')
async def get_item_process(*,user: Users = Depends(get_current_user),item_id: int) :
    with get_session() as session :
        try :
            item: Items = session.query(Items).get(item_id)
            if (item.user_id != user.id) and (not item.isPublic) :
                res = resp_400(msg='该用户没有访问该商品id的权限')
            else :
                process_links = item.process_links
                process_links = sorted(process_links,key=lambda x : x.order)
                process_ls = []
                for process_link in process_links :
                    process_ls.append(process_link.process.dict())
                res = resp_200(data=process_ls,msg="获取商品工序成功")
        except Exception as e :
            logger.error(f'获取商品工序失败,因为：{e}')
            res = resp_500(msg="数据库操作错误")
    return res

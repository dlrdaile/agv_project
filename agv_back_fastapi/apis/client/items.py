"""
author:dlr123
date:2022年06月12日
"""
import uuid
from pathlib import Path
from core.config import settings
from fastapi import APIRouter,Request,UploadFile,Depends
from core.security import get_current_user
from db.session import get_session
from models.item.items import Items
from models.user.users import Users
from utils.resp_code import resp_200,resp_500
from core.logger import logger
items_api = APIRouter(prefix='/items')


@items_api.post('/add')
def add_item(req: Request,file: UploadFile,user: Users = Depends(get_current_user)) :
    img_store_dir = Path(settings.PROJECT_ROOT_PATH)
    file_path = Path(file.filename)
    img_uuid = str(uuid.uuid1())
    filename = img_uuid + file_path.suffix
    img_path = img_store_dir / f'static/img/{filename}'
    img_path.write_bytes(file.file.read())
    with get_session() as session :
        try:
            img_store_url = f"{settings.BASE_URL}/static/img/{filename}"
            items = Items(**req._form._dict)
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


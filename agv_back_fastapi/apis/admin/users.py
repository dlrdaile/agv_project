"""
author:dlr123
date:2022年06月28日
"""
from fastapi import APIRouter,Depends
from fastapi.encoders import jsonable_encoder

from core.logger import logger
from core.security import get_current_user
from crud.orders import orderCrud
from db.session import get_session
from models.item.items import UserOrder
from models.user.users import Users
from schemas.orders import CreateOrder,UpdateOrder,QueryOrder,OutputOrder
from utils.resp_code import resp_200,resp_500,resp_400

user_api = APIRouter(prefix='/user')

@user_api.get('/getuserlist')
async def get_user_list(user: Users = Depends(get_current_user)):
    if user.isAdmin:
        with get_session() as session:
            try:
                all_user:list[Users] = session.query(Users).filter(Users.id != 1).all()
                res_data = [{'id':user.id,'name':user.name} for user in all_user]
                return resp_200(data=res_data,msg='获取用户名列表成功')
            except Exception as e:
                logger.error(f'获取用户名列表失败错误,因为：{e}')
                return resp_500(msg="数据库操作错误")

        pass
    else:
        raise PermissionError("没有权限获得所有用户")
    pass
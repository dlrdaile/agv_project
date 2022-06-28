"""
author:dlr123
date:2022年06月07日
"""
from fastapi import APIRouter,Depends
from sqlmodel import select
from typing import Optional
from core.logger import logger
from core.security import get_current_user
from db import get_session
from models.item.process import Process
from models.user.address import Provincial
from models.user.users import Users
from schemas.user import OutputUser
from utils.resp_code import resp_200,resp_500,resp_400
from utils.custom_exc import UserNotExist,PermissionNotEnough

commons_api = APIRouter(prefix="/commons")


@commons_api.get('/userinfo')
async def get_user_info(user: Users = Depends(get_current_user),user_id:Optional[int]=None) :
    if user_id is not None:
        if user.isAdmin:
            with get_session() as session:
                try:
                    client_info = session.query(Users).get(user_id)
                    if client_info is not None:
                        data = OutputUser.from_orm(client_info)
                    else:
                        raise UserNotExist("请求的用户不存在")
                except Exception as e:
                    session.rollback()
                    logger.error(f'用户信息获取失败,因为：{e}')
                    raise e
        else:
            raise PermissionNotEnough("你没有访问其他用户信息的权限")
    else:
        data = OutputUser.from_orm(user)
    data.roles = ["admin",] if user.isAdmin else ["client",]
    return resp_200(data=data)


@commons_api.get('/maplist')
async def get_map_list() :
    data = []
    with get_session() as session :
        sql = select(Provincial)
        result = session.exec(sql).all()
        for province in result :
            p_data = {}
            p_data['label'] = province.name
            p_data['value'] = province.id
            c_data = []
            for city in province.cities :
                c_data.append({
                    'label' : city.name,
                    'value' : city.union_id
                })
            if c_data != [] :
                p_data['children'] = c_data
            data.append(p_data)
    return resp_200(data=data,msg="成果获得地理信息列表")


@commons_api.get('/processlist')
async def get_process_list() :
    with get_session() as session :
        try :
            query_result = session.query(Process).all()
            process_list = [process.dict() for process in query_result]
            return resp_200(data=process_list,msg='成功获得加工信息')
        except :
            session.rollback()
            logger.error('获得工艺信息失败')
            return resp_500(msg=f'数据库连接失败！')

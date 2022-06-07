"""
author:dlr123
date:2022年06月07日
"""
from fastapi import APIRouter,Depends
from sqlmodel import select
from core.security import get_current_user
from crud.base import CRUDBase
from db import get_session
from models.user.address import Provincial
from models.user.users import Users
from schemas.user import OutputUser
from utils.resp_code import resp_200

commons_api = APIRouter(prefix="/commons")


@commons_api.get('/userinfo')
async def get_user_info(user: Users = Depends(get_current_user)) :
    data = OutputUser.from_orm(user)
    data.roles = ["admin",] if data.isAdmin else ["client",]
    return resp_200(data=data)


@commons_api.get('/maplist')
async def get_map_list() :
    data = []
    with get_session() as session:
        sql = select(Provincial)
        result = session.exec(sql).all()
        for province in result:
            p_data = {}
            p_data['label'] = province.name
            p_data['value'] = province.id
            c_data = []
            for city in province.cities:
                c_data.append({
                    'label':city.name,
                    'value':city.union_id
                })
            if c_data != []:
                p_data['children'] = c_data
            data.append(p_data)
    return resp_200(data=data,msg="成果获得地理信息列表")

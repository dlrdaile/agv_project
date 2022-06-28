"""
author:dlr123
date:2022年06月14日
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

order_api = APIRouter(prefix='/order')


@order_api.post('/create')
def create_order(*,create_data: CreateOrder,user: Users = Depends(get_current_user)) :
    with get_session() as session:
        try:
            order = UserOrder.from_orm(create_data)
            session.add(order)
            session.commit()
            return resp_200(msg="订单创建成功")
        except Exception as e:
            session.rollback()
            logger.error(f'订单创建失败,因为：{e}')
            return resp_500(msg="数据库操作错误")


@order_api.post('/update')
def update_order(*,update_data: UpdateOrder,user: Users = Depends(get_current_user)) :
    result = orderCrud.update_order(user,update_data)
    if result != 0:
        return resp_200(msg="商品信息修改成功")
    else:
        return resp_400(msg="修改信息失败")


@order_api.post('/getlist')
async def get_order_list(query_data: QueryOrder,user: Users = Depends(get_current_user)) :
    with get_session() as session :
        try :
            query_sql = orderCrud.query_data(user,query_data)
            count_sql = orderCrud.get_count(user,query_data)
            results: list[UserOrder] = session.exec(query_sql).all()
            total = session.exec(count_sql).first()
            order_list = []
            for result in results :
                output_order = OutputOrder.from_orm(result)
                output_order.item_name = result.item.name
                output_order_dict = output_order.dict()
                output_order_dict['user_name'] = result.user.name
                order_list.append(output_order_dict)
            output_data = {'orderlist' : order_list,'total' : total}
            return resp_200(data=jsonable_encoder(output_data),msg='获取订单数据成功')
        except Exception as e :
            logger.error(f'获取订单列表时数据库查询错误，原因是{e}')
            return resp_500(msg='数据库查询错误')


@order_api.delete('/delete')
async def delete_order(*,order_id: int,user: Users = Depends(get_current_user)) :
    issucess,reason = orderCrud.delete_order(user,order_id)
    if issucess :
        return resp_200(msg='删除成功')
    else :
        return resp_400(msg=f'删除失败，因为:{reason}')
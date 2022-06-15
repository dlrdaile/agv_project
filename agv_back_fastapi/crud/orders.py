"""
author:dlr123
date:2022年06月15日
"""

from sqlalchemy import desc,delete,update
from sqlmodel import select,Session,func

from crud.base import CRUDBase
from db.session import get_session
from models import Users
from models.item.items import UserOrder
from schemas.orders import CreateOrder,UpdateOrder
from schemas.orders import QueryOrder


class OrderCrud(CRUDBase[UserOrder,UpdateOrder,CreateOrder]) :
    def __init__(self) :
        super(OrderCrud,self).__init__(UserOrder)

    def query_data(self,user: Users,query: QueryOrder) :
        if user.isAdmin :
            sql = select(self.model)
        else :
            sql = select(self.model).where(user.id == self.model.user_id).where(self.model.IsShowToClient)
        sql = self.filter_order(sql,query)
        pageIndex = query.page
        pageSize = query.limit
        if not (pageIndex == -1 and pageSize == -1) :
            sql = sql.offset((pageIndex - 1)*pageSize).limit(pageSize)
        if query.desc :
            sql = sql.order_by(desc(self.model.id))
        else :
            sql = sql.order_by(self.model.id)
        return sql

    def filter_order(self,sql,query: QueryOrder) :
        if query.item_id :
            sql = sql.where(self.model.item_id.in_(query.item_id))
        if query.editState :
            sql = sql.where(self.model.isEditing == query.editState)
        if query.orderState :
            sql = sql.where(self.model.status.in_(query.orderState))
        if query.isShowToClient :
            sql = sql.where(self.model.IsShowToClient == query.isShowToClient)
        return sql

    def get_count(self,user: Users,query: QueryOrder) :
        if user.isAdmin :
            sql = select(func.count(self.model.id))
        else :
            sql = select(func.count(self.model.id)).where(user.id == self.model.user_id).where(
                self.model.IsShowToClient)
        sql = self.filter_order(sql,query)
        return sql

    def delete_order(self,user: Users,order_id: int,db: Session = get_session()) :
        sucess = True
        reason = None
        try :
            if user.isAdmin :
                sql = delete(self.model).where(self.model.id == order_id)
                db.execute(sql)
                db.commit()
            else :
                order: UserOrder = db.query(self.model).get(order_id)
                order.IsShowToClient = False
                db.add(order)
                db.commit()
        except Exception as e :
            reason = e
            db.rollback()
        finally :
            db.close()
        return sucess,reason

    def update_order(self,update_data:UpdateOrder,db: Session = get_session()):
        """ 通过 id 更新对象 """
        obj_data = update_data.dict(exclude={'id',},exclude_none=True)
        sql = update(self.model).where(self.model.id == update_data.id).values(obj_data)
        result = db.execute(sql).rowcount
        db.commit()
        db.close()
        return result
orderCrud = OrderCrud()

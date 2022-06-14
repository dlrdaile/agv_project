"""
author:dlr123
date:2022年06月13日
"""
from typing import Optional,List

from sqlalchemy import desc,and_
from sqlmodel import select,Session,or_,func

from crud.base import CRUDBase
from db.session import get_session
from models import Users
from models.item.items import Items
from schemas.items import CreateItem,UpdateItem


class ItemCrud(CRUDBase[Items,UpdateItem,CreateItem]) :
    def __init__(self) :
        super(ItemCrud,self).__init__(Items)

    def get_by_name(self,name: str,db: Session = get_session()) -> Optional[Items] :
        """ 通过名字得到用户 """
        sql = select(self.model).where(self.model.name == name)
        result = db.scalar(sql)
        db.close()  # 释放会话
        return result

    def get_id_by_name(self,name: str,db: Session = get_session()) -> Optional[int] :
        result = self.get_by_name(name,db)
        return result.id

    def get_multi(self,query: str,user: Users,db: Session = get_session(),
                  pageIndex: int = 1,
                  pageSize: int = 10) -> List[Items] :
        if user.isAdmin :
            sql = select(self.model)
        else :
            sql = select(self.model).where(or_(self.model.isPublic,
                                               self.model.user_id == user.id)).where(self.model.IsShowToClient)
        sql = self.process_query(query,sql,user)
        if not (pageIndex == -1 and pageSize == -1) :
            sql = sql.offset((pageIndex - 1)*pageSize).limit(pageSize)
        sql = sql.order_by(
            desc(self.model.id))
        result = db.scalars(sql).all()
        db.close()  # 释放会话
        return result

    def process_query(self,query: str,sql,user: Users) :
        if query == 'admin' :
            sql = sql.where(self.model.Provider == 'admin')
        elif query == 'third' :
            if user.isAdmin :
                sql = sql.where(self.model.Provider != 'admin')
            else :
                sql = sql.where(and_(self.model.Provider != 'admin',self.model.user_id != user.id))
        elif query == 'self' :
            sql = sql.where(self.model.user_id == user.id)
        return sql

    def get_count(self,user: Users,query:str ,db: Session = get_session()) -> int :
        if user.isAdmin :
            sql = select(func.count(self.model.id))
        else :
            sql = select(func.count(self.model.id)).where(or_(self.model.isPublic,user.id == self.model.user_id)).where(self.model.IsShowToClient)
        sql = self.process_query(query,sql,user)
        count = db.exec(sql).first()
        db.close()
        return count


itemCrud = ItemCrud()

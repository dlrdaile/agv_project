#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/14 17:00
# @Author : zxiaosi
# @desc : 封装数据库增删改查方法
from typing import Any,Dict,Generic,List,Optional,Type,TypeVar,Union

from sqlmodel import Session,SQLModel
from sqlmodel import func,distinct,select,insert,update,desc,delete

from db.session import get_session

ModelType = TypeVar("ModelType",bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType",bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType",bound=SQLModel)


class CRUDBase(Generic[ModelType,CreateSchemaType,UpdateSchemaType]) :
    """ CRUD 增 查 改 删 """

    def __init__(self,model: Type[ModelType]) :
        self.model = model

    def get(self,id: Any,db: Session = get_session()) -> Optional[ModelType] :
        """ 通过 id 获取对象 """
        sql = select(self.model).where(self.model.id == id)
        result = db.scalar(sql)
        db.close()  # 释放会话
        return result

    def get_multi(self,db: Session = get_session(),pageIndex: int = 1,pageSize: int = 10) -> List[ModelType] :
        """ 获取第 pageIndex 页的 pageSize 数据 """
        if pageIndex == -1 and pageSize == -1 :
            sql = select(self.model).order_by(desc(self.model.id))
        else :
            sql = select(self.model).offset((pageIndex - 1)*pageSize).limit(pageSize).order_by(desc(self.model.id))
        result = db.scalars(sql)
        db.close()  # 释放会话
        return result.all()

    def get_number(self,db: Session = get_session()) -> int :
        """ 获取表的总条数 """
        sql = select(func.count(distinct(self.model.id)))
        result = db.scalar(sql)
        db.close()  # 释放会话
        return result

    def create(self,obj_in: CreateSchemaType,db: Session = get_session()) -> int :
        """ 添加对象 """
        try:
            insert_data = self.model.from_orm(obj_in).dict()
            sql = insert(self.model).values(insert_data)
            result = db.execute(sql)
            db.commit()
        except:
            db.rollback()
        finally:
            db.close()

    def update(self,name: str,obj_in: Union[UpdateSchemaType,Dict[str,Any]],db: Session = get_session()) -> int :
        """ 通过 id 更新对象 """
        if isinstance(obj_in,dict) :  # 判断对象是否为字典类型(更新部分字段)
            obj_data = obj_in
        else :
            obj_data = obj_in.dict()
        sql = update(self.model).where(self.model.name == name).values(obj_data)
        result = db.execute(sql)
        db.commit()
        db.close()

    async def remove(self,id: int,db: Session = get_session()) -> int :
        """ 通过 id 删除对象 """
        sql = delete(self.model).where(self.model.id == id)
        result = db.execute(sql)
        db.commit()
        db.close()
        return result.rowcount

    def remove_multi(self,id_list: list,db: Session = get_session()) :
        """ 同时删除多个对象 """
        id_list = [int(i) for i in id_list]  # postgresql 字段类型限制
        sql = delete(self.model).where(self.model.id.in_(id_list))
        result = db.execute(sql)
        db.commit()
        db.close()
        return result.rowcount

    def get_multi_relation(self,db: Session = get_session()) :
        """ 获取关系字段 """
        sql = select(self.model.id,self.model.name).order_by(desc(self.model.id)).distinct()
        result = db.exec(sql)
        db.close()
        return result.all()

    def sort(self,name: str,pageIndex: int = 1,pageSize: int = 10,db: Session = get_session()) -> List[ModelType] :
        """ 验证用户 """
        filed_name = self.model.__table__.c[name]
        if pageIndex == -1 and pageSize == -1 :
            sql = select(self.model).order_by(desc(filed_name))
        else :
            sql = select(self.model).offset((pageIndex - 1)*pageSize).limit(pageSize).order_by(desc(filed_name))
        result = db.scalars(sql)
        db.close()  # 释放会话
        return result.all()

    def get_all(self,db: Session = get_session()):
        sql = select(self.model).order_by(self.model.id)
        result = db.execute(sql).all()
        db.close()
        return result

"""
author:dlr123
date:2022年05月31日
"""
from typing import Optional

from sqlmodel import select,Session
from models import Users
from schemas import UpdateUser,CreateUser

from crud.base import CRUDBase
from core.security import verify_password
from db.session import get_session



class UserCrud(CRUDBase[Users,UpdateUser,CreateUser]) :
    def __init__(self) :
        super(UserCrud,self).__init__(Users)

    def get_by_name(self,name: str,db: Session=get_session()) -> Optional[Users] :
        """ 通过名字得到用户 """
        sql = select(self.model).where(self.model.name == name)
        result = db.scalar(sql)
        db.close()  # 释放会话
        return result

    def authenticate(self,username: str,password: str) -> Optional[Users] :
        """ 验证用户 """
        user = self.get_by_name(name=username)
        if not user :
            return None
        if not verify_password(password,user.hashed_password) :
            return None
        return user


userCrud = UserCrud()
if __name__ == "__main__" :
    print(userCrud.get_by_name("admin").dict())

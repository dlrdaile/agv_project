"""
author:dlr123
date:2022年05月31日
"""
from typing import Optional

from sqlmodel import select,Session

from core.security import verify_password
from crud.base import CRUDBase
from db.session import get_session
from models import Users
from schemas import UpdateUser,CreateUser
from utils.custom_exc import ErrorUser

class UserCrud(CRUDBase[Users,UpdateUser,CreateUser]) :
    def __init__(self) :
        super(UserCrud,self).__init__(Users)

    def get_by_name(self,name: str,db: Session = get_session()) -> Optional[Users] :
        """ 通过名字得到用户 """
        sql = select(self.model).where(self.model.name == name)
        result = db.scalar(sql)
        db.close()  # 释放会话
        return result

    def authenticate(self,username: str,password: str) -> Optional[Users] :
        """ 验证用户 """
        user = self.get_by_name(name=username)
        if not user :
            raise ErrorUser("用户不存在")
        if not verify_password(password,user.hashed_password) :
            raise ErrorUser("密码错误")
        return user

    def get_by_email(self,email: str,db: Session = get_session()) -> Optional[Users] :
        sql = select(self.model).where(self.model.email == email)
        result = db.scalar(sql)
        db.close()
        return result


userCrud = UserCrud()
if __name__ == "__main__" :
    print(userCrud.get_by_name("admin").dict())

"""
author:dlr123
date:2022年06月12日
"""
import random
from datetime import datetime

import numpy as np
from faker import Faker

from core.logger import logger
from core.security import get_password_hash
from models.item.items import Items
from models.item.links import ItemProcessLink
from models.item.process import Process
from models.user.address import City
from models.user.users import Users
from utils.random_choose import choose_process
from .session import get_session

fake_ch = Faker(locale='zh_CN')
fake_en = Faker(locale='en_US')


def create_fake_users() :
    user_list = []
    fake_user_num = 100
    with get_session() as session :
        city_num = session.query(City).count()
        city_id_list = (np.arange(city_num) + 1).tolist()
        try :
            for _ in range(fake_user_num) :
                isActive = fake_ch.boolean()
                if isActive :
                    last_active_time = datetime.now()
                else :
                    last_active_time = fake_ch.past_datetime('-1y')
                create_time = fake_ch.past_datetime('-5y')
                while create_time > last_active_time :
                    create_time = fake_ch.past_datetime('-5y')
                userInfo = Users(name=fake_ch.user_name(),
                                 hashed_password=get_password_hash('123456'),
                                 create_time=create_time,
                                 nickname=fake_ch.name(),
                                 last_active_time=last_active_time,
                                 isActive=isActive,
                                 email=fake_ch.email(),
                                 phone=fake_ch.phone_number(),
                                 address_id=random.choice(city_id_list))
                user_list.append(userInfo)
            session.add_all(user_list)
            session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'假的用户信息初始化失败,因为：{e}')
        else :
            logger.info('假的用户信息初始化成功')
    pass


def create_fake_items() :
    user_num = 10
    max_item_num = 5
    min_item_num = 1
    min_process_num = 2
    max_process_num = 6
    with get_session() as session :
        try :
            process_num = session.query(Process).count()
            user_count = session.query(Users).count()
            user_id_list = np.random.choice(np.arange(2,user_count + 1),user_num).tolist()
            for user_id in user_id_list :
                item_ls = []
                item_process_link_ls = []
                item_num = random.randint(min_item_num,max_item_num)
                user: Users = session.query(Users).get(user_id)
                user_name = user.nickname
                for i in range(item_num) :
                    image_path = 'https://picsum.photos/300'
                    item = Items(
                                 name=f'{user_name}的商品{i + 1}',
                                 description=fake_ch.text(max_nb_chars=100,ext_word_list=None),
                                 image_path=image_path,
                                 Provider=user_name,
                                 price=random.randint(100,500),
                                 isPublic=fake_ch.boolean(),
                                 weight=random.randint(1,10),
                                 user_id=user_id)
                    process_queue_ls = choose_process(min_process_num,max_process_num,process_num)
                    for order,process_id in enumerate(process_queue_ls) :
                        item_process_link = ItemProcessLink(process_id=process_id,
                                                            order=order)
                        item.process_links.append(item_process_link)
                        item_process_link_ls.append(item_process_link)
                    item_ls.append(item)
                session.add_all(item_ls)
                session.add_all(item_process_link_ls)
            session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'假的商品数据初始化失败,因为：{e}')
        else :
            logger.info('假的商品数据初始化成功')


# todo:造一些假的订单
def create_fake_user_items() :

    pass


# todo:造一些假的任务记录
def create_fake_tasks() :
    pass


async def create_fake() :
    create_fake_users()
    create_fake_items()
    create_fake_user_items()
    create_fake_tasks()

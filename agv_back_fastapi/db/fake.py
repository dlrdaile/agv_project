"""
author:dlr123
date:2022年06月12日
"""
import random
from datetime import datetime

import numpy as np
from faker import Faker
from sqlalchemy import not_,or_
from sqlmodel import select

from core.logger import logger
from core.security import get_password_hash
from models.car.tasks import Tasks,TaskStatus
from models.item.items import Items
from models.item.items import UserOrder,OrderStatus
from models.item.links import ItemProcessLink
from models.item.links import TaskEquipmentLink
from models.item.links import SubTaskStatus
from models.item.process import Process
from models.user.address import City
from models.user.users import Users
from utils.random_choose import choose_process
from .session import get_session

fake_ch = Faker(locale='zh_CN')
fake_en = Faker(locale='en_US')
random.seed(42)
np.random.seed(42)
fake_ch.random.seed(42)
fake_en.random.seed(42)
def create_fake_users() :
    user_list = []
    fake_user_num = 100
    with get_session() as session :
        city_num = session.query(City).count()
        city_id_list = (np.arange(city_num) + 1).tolist()
        try :
            for _ in range(fake_user_num) :
                isActive = fake_ch.boolean()
                time_delta = fake_ch.time_delta(2000)
                create_time = datetime.now() - time_delta
                if isActive :
                    last_active_time = datetime.now()
                else :
                    last_active_time = create_time + fake_ch.time_delta(time_delta)
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
                delta_time = user.last_active_time - user.create_time
                for i in range(item_num) :
                    item_create_time = user.create_time + fake_ch.time_delta(delta_time)
                    image_path = 'https://picsum.photos/200'
                    item = Items(name=f'{user_name}的商品{i + 1}',
                                 description=fake_ch.text(max_nb_chars=100,ext_word_list=None),
                                 image_path=image_path,
                                 Provider=user_name,
                                 price=random.randint(100,500),
                                 isPublic=fake_ch.boolean(),
                                 weight=random.randint(1,10),
                                 create_time=item_create_time,
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
def create_fake_user_orders() :
    min_order_num = 0
    max_order_num = 200
    create_num = 0
    create_user_num = 0
    with get_session() as session :
        try :
            clients: list[Users] = session.query(Users).filter(not_(Users.isAdmin)).all()
            for client in clients :
                sql = select(Items).where(Items.create_time <= client.create_time).where(or_(Items.isPublic,
                                                                                             Items.user_id == client.id))
                can_use_items = session.exec(sql).all()
                order_num = random.randint(min_order_num,max_order_num)
                states_ls = np.random.choice([0,2,3,4],order_num,replace=True,p=[0.3,0.1,0.59,0.01])
                if len(can_use_items) == 0 :
                    logger.warning('a user has not item can use!')
                    continue
                order_list = []
                for i in range(order_num) :
                    isEdit = False
                    if states_ls[i] == OrderStatus.NotProcessed :
                        isEdit = fake_ch.boolean()
                    choosed_item = random.choice(can_use_items)
                    time_delta1 = datetime.now() - choosed_item.create_time
                    create_time = choosed_item.create_time + fake_ch.time_delta(time_delta1)
                    user_order = UserOrder(name=fake_en.pystr(10,15),
                                           status=states_ls[i],
                                           isEditing=isEdit,
                                           create_time=create_time,
                                           user_id=client.id,
                                           item_id=choosed_item.id,
                                           description=fake_ch.text(max_nb_chars=100,ext_word_list=None),
                                           )
                    if user_order.status == OrderStatus.Finished or user_order.status == OrderStatus.Fail :
                        time_delta2 = datetime.now() - create_time
                        user_order.start_time = create_time + fake_ch.time_delta(time_delta2)

                        time_delta3 = datetime.now() - user_order.start_time
                        user_order.end_time = user_order.start_time + fake_ch.time_delta(time_delta3)
                    if user_order.status == OrderStatus.Reject or user_order.status == OrderStatus.Fail :
                        user_order.reject_or_fail_reason = fake_ch.text(max_nb_chars=30,ext_word_list=None)
                    order_list.append(user_order)
                create_user_num += 1
                create_num += order_num
                session.add_all(order_list)
            session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'假的订单数据初始化失败,因为：{e}')
        else :
            logger.info(f'假的订单数据初始化成功，共为{create_user_num}个用户创建了{create_num}订单')


# todo:造一些假的任务记录
def create_fake_tasks() :
    with get_session() as session :
        try :
            sql = select(UserOrder).where(or_(UserOrder.status == OrderStatus.Finished,UserOrder.status == OrderStatus.Fail))  # 获得状态会完成和失败的数据
            orders = session.exec(sql).all()
            for order in orders :
                description = fake_ch.text(max_nb_chars=100,ext_word_list=None)
                task = Tasks(create_time=order.start_time,
                             end_time=order.end_time,
                             description=description,
                             )
                # task.start_time = fa
                time_delta = order.end_time - order.start_time
                task.start_time = order.start_time + fake_ch.time_delta(time_delta)
                order.task = task
                order.task_description = description
                process_links = order.item.process_links
                if order.status == OrderStatus.Finished :
                    task.status = TaskStatus.SUCCEEDED
                else :
                    task.fail_reason = fake_ch.text(max_nb_chars=30,ext_word_list=None)
                    task.status = TaskStatus.FAIL
                    process_num = len(process_links)
                    fail_node = random.choice(range(process_num))

                task_equip_link_ls = []
                process_links = sorted(process_links,key=lambda x:x.order)
                for index,process_link in enumerate(process_links) :
                    # 添加顺序
                    task_equip_link = TaskEquipmentLink(order=process_link.order)
                    if order.status == OrderStatus.Finished:
                        task_equip_link.status = SubTaskStatus.SUCCEEDED
                    else:
                        if index < fail_node:
                            task_equip_link.status = SubTaskStatus.SUCCEEDED
                        else:
                            task_equip_link.status = SubTaskStatus.FAIL
                    # 选择设备
                    alterEquipments = process_link.process.equipment
                    selected_equipment = random.choice(alterEquipments)
                    task_equip_link.equipment = selected_equipment
                    task_equip_link.task = task #必须再有外键的地方添加才行
                    task_equip_link_ls.append(task_equip_link)
                session.add(order)
                session.add(task)
                session.add_all(task_equip_link_ls)
            session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'假的任务数据初始化失败,因为：{e}')
        else :
            logger.info(f'假的任务数据初始化成功')


async def create_fake() :
    create_fake_users()
    create_fake_items()
    create_fake_user_orders()
    create_fake_tasks()

"""
author:dlr123
date:2022年06月12日
"""
import datetime
import os.path
import random

from faker import Faker
from core.logger import logger
from core.security import get_password_hash
from crud.user import userCrud
from models import CarStatus,Cars,Odom,Laser,Imu,Battery,Press,Camera,DeviceTypeLink,DeviceType,DeviceStatus
from models.item.equipment import Equipment
from models.item.items import Items
from models.item.links import ItemProcessLink
from models.item.process import Process
from models.user import Users
from .fake import create_fake
from .session import get_session
from utils.random_choose import choose_process

fake = Faker(locale='zh_CN')


def init_user() :
    with get_session() as session :
        try :
            user = userCrud.get_by_name('admin')
            if user is None :
                adminInfo = Users(id=1,
                                  name='admin',
                                  hashed_password=get_password_hash('123456'),
                                  create_time=datetime.datetime.now() - datetime.timedelta(2000),
                                  isAdmin=True,
                                  nickname='admin',
                                  email='965794928@qq.com',
                                  phone='18978911249',
                                  address_id=1)
                session.add(adminInfo)
                session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'管理者信息初始化失败,因为：{e}')
        else :
            logger.info('管理者信息初始化成功')


def init_process() :
    datas = [(1,'车',fake.paragraph(nb_sentences=3,variable_nb_sentences=True,ext_word_list=None)),
             (2,'洗',fake.paragraph(nb_sentences=3,variable_nb_sentences=True,ext_word_list=None)),
             (3,'磨',fake.paragraph(nb_sentences=3,variable_nb_sentences=True,ext_word_list=None)),
             (4,'钻',fake.paragraph(nb_sentences=3,variable_nb_sentences=True,ext_word_list=None))]
    process_ls = []
    with get_session() as session :
        try :
            for data in datas :
                process = Process(id=data[0],name=data[1],description=data[2])
                process_ls.append(process)
            session.add_all(process_ls)
            session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'工艺数据初始化失败,因为:{e}')
        else :
            logger.info('工艺数据初始化成功')


def init_equipment() :
    """
        初始化设备信息
    """
    datas = [(1,'沈阳机床厂1号',fake.paragraph(nb_sentences=3,variable_nb_sentences=True,ext_word_list=None)),
             (2,'长沙机床1号',fake.paragraph(nb_sentences=3,variable_nb_sentences=True,ext_word_list=None)),
             (3,'武汉激光加工3号',fake.paragraph(nb_sentences=3,variable_nb_sentences=True,ext_word_list=None)),
             (4,'德国机床5号',fake.paragraph(nb_sentences=3,variable_nb_sentences=True,ext_word_list=None))]
    relationship = [(1,2),(2,),(4,),(1,3)]
    coordinate = [(-0.75,-2.97,-171.42),
                  (-6.48,-2.21,88.83),
                  (-4.83,2.12,-7.38),
                  (0.33,2.14,-86.06)]
    equipment_ls = []
    with get_session() as session :
        try :
            for index,data in enumerate(datas) :
                equipment = Equipment(id=data[0],
                                      name=data[1],
                                      description=data[2],
                                      equipStatus=0,
                                      x=coordinate[index][0],
                                      y=coordinate[index][1],
                                      yaw=coordinate[index][2],
                                      floor=1
                                      )
                for process_id in relationship[index] :
                    equipment.process.append(session.query(Process).get(process_id))
                equipment_ls.append(equipment)
            session.add_all(equipment_ls)
            session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'设备数据初始化失败,因为：{e}')
        else :
            logger.info('设备数据初始化成功')


def init_items() :
    init_item_num = 5
    item_ls = []
    item_process_link_ls = []
    with get_session() as session :
        process_num = session.query(Process).count()
        min_process_num = 2
        max_process_num = 6
        try :
            for i in range(init_item_num) :
                # req = requests.get('https://www.dmoe.cc/random.php?return=json')
                # if req.status_code == 200 :
                #     json_data = req.json()
                #     image_path = json_data['imgurl']
                image_path = 'https://picsum.photos/200'
                admin_user: Users = session.query(Users).get(1)
                fake_time = admin_user.create_time
                item = Items(name=f'商品{i + 1}',
                             description=fake.text(max_nb_chars=100,ext_word_list=None),
                             image_path=image_path,
                             price=random.randint(100,500),
                             weight=random.randint(1,10),
                             create_time=fake_time,
                             user_id=1)
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
            logger.error(f'商品数据初始化失败,因为：{e}')
        else :
            logger.info('商品数据初始化成功')


def init_map_data() :
    with open(os.path.join(os.getcwd(),'mapData.sql'),'rt',encoding='utf-8') as f :
        with get_session() as session :
            try :
                for line in f :
                    try :
                        session.exec(line.strip())
                    except :
                        pass
                session.commit()
            except Exception as e :
                session.rollback()
                logger.error(f'地理信息初始化失败,因为：{e}')
            else :
                logger.info('地理信息初始化成功')


def init_device() :
    device_type_names = ["激光雷达","双目相机","里程计","倾角传感器","电池","压力传感器"]
    with get_session() as session :
        try :
            device_type = []
            for i,device_type_name in enumerate(device_type_names) :
                device_type.append(DeviceType(id=i + 1,
                                              name=device_type_name,
                                              description=fake.paragraph(nb_sentences=3,
                                                                         variable_nb_sentences=True,
                                                                         ext_word_list=None)))
            session.add_all(device_type)
            session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'小车设备数据初始化失败,因为：{e}')
        else :
            logger.info('小车设备数据初始化成功')


def init_carInfo() :
    with get_session() as session :
        try :
            for i in range(1) :
                data = dict(name=f"dl_agv",productor="戴乐",isSimulation=True,
                            description=fake.paragraph(nb_sentences=3,
                                                       variable_nb_sentences=True,
                                                       ext_word_list=None),
                            status=CarStatus.INACTIVATE,
                            ip="192.168.10.47",
                            port="9090",
                            weight=20
                            )
                car = Cars(**data)
                odom = Odom(**dict(name="里程计",topicName="/odom",topicType="nav_msgs/Odometry"))
                laser = Laser(**dict(name="激光雷达",topicName="/scan",topicType="sensor_msgs/LaserScan"))
                imu = Imu(**dict(name="倾角传感器",topicName="/imu",topicType="sensor_msgs/Imu"))
                battery = Battery(**dict(name="电池",topicName="/battery",topicType="communicate_with_stm32/BatteryInfo",
                                         currentBattery=11))
                press = Press(**dict(name="压力传感器",topicName="/press",topicType="communicate_with_stm32/Pressinfo"))
                cameraLeft = Camera(**dict(name="双目相机左",topicName="/multisense_sl/camera/left/image_raw/compressed",
                                           topicType="sensor_msgs/CompressedImage"))
                cameraRight = Camera(**dict(name="双目相机右",topicName="/multisense_sl/camera/right/image_raw/compressed",
                                            topicType="sensor_msgs/CompressedImage"))
                odom_link = DeviceTypeLink(type_id=3)
                laser_link = DeviceTypeLink(type_id=1)
                imu_link = DeviceTypeLink(type_id=4)
                battery_link = DeviceTypeLink(type_id=5)
                press_link = DeviceTypeLink(type_id=6)
                cameraR_link = DeviceTypeLink(type_id=2)
                cameraL_link = DeviceTypeLink(type_id=2)
                odom_link.odom_link = odom
                laser_link.laser_link = laser
                imu_link.imu_link = imu
                battery_link.battery_link = battery
                press_link.press_link = press
                cameraR_link.camera_link = cameraRight
                cameraL_link.camera_link = cameraLeft
                device_link = [battery_link,imu_link,press_link,cameraR_link,cameraL_link,odom_link,laser_link]
                car.devices.extend(device_link)
                session.add(car)
                session.add_all([odom,battery,press,laser,imu,cameraRight,cameraLeft])
                session.add_all(device_link)
            session.commit()
        except Exception as e :
            session.rollback()
            logger.error(f'小车数据初始化失败,因为：{e}')
        else :
            logger.info('小车数据初始化成功')


async def init_data() :
    """ 初始化表数据 """
    init_user()
    init_map_data()
    init_process()
    init_equipment()
    init_items()
    init_device()
    init_carInfo()
    await create_fake()

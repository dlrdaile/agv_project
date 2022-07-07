import datetime
from typing import Optional

import actionlib
import rospy
from agv_nav.msg import *
from geometry_msgs.msg import Pose
from std_msgs.msg import String
from tf.transformations import quaternion_from_euler
from actionlib_msgs.msg import GoalID
from core.logger import logger
from db.session import Session
from models.car.car import Cars, CarStatus
from models.car.tasks import Tasks, TaskStatus
from models.item.items import OrderStatus, UserOrder
from models.item.links import TaskEquipmentLink, SubTaskStatus
from models.item.equipment import EquipmentStatus

class TaskExecutionNode():
    def __init__(self, namespace: str, car_name: str) -> None:
        # self.sub = rospy.Subscriber(f"{name}/chatter", String, self.callback, queue_size=10)
        # self.pub = rospy.Publisher(f"{name}/pub", String, queue_size=10)
        self.client = actionlib.SimpleActionClient(car_name, TaskListAction)
        self.goalList = TaskListGoal()
        self.goalList.task_pose_list.header.frame_id = "map"
        self.current_task: Optional[Tasks] = None
        self.car_name = car_name
        self.session: Optional[Session] = None
        self.task: Optional[Tasks] = None
        self.car: Optional[Cars] = None
        self.user_order: Optional[UserOrder] = None
        self.subTaskStatus = []
        self.task_equipment_links: list[TaskEquipmentLink] = []
        self.finished = False

    # def callback(self, msg):
    #     rospy.loginfo("I heard:%s", msg.data)

    def done_cb(self, state: actionlib_msgs.msg.GoalStatus, result: TaskListResult):
        if state == 2:
            self.car.status = CarStatus.PAUSE
            logger.warning(f"the task {self.task.id} has been paused!")
            rospy.logwarn(f"the task {self.task.id} has been paused!")
        elif state == 3:
            end_time = datetime.datetime.now()
            self.car.status = CarStatus.FREE
            self.task.status = TaskStatus.SUCCEEDED
            self.task.end_time = end_time
            self.user_order.end_time = end_time
            self.user_order.status = OrderStatus.Finished
            self.car.current_task_id = None
            logger.info(f"{self.car.name} sucess to finish the task {self.task.id}!")
            rospy.loginfo(f"{self.car.name} sucess to finish the task {self.task.id}!")
        for i, equiment_link in enumerate(self.task_equipment_links):
            equiment_link.status = result.task_final_status[i]
            equiment_link.equipment.equipStatus = EquipmentStatus.Free
        self.session.add_all(self.task_equipment_links)
        self.session.add(self.car)
        self.session.add(self.user_order)
        self.session.add(self.task)
        self.session.commit()
        self.finished = True

    def active_cb(self):
        self.car.status = CarStatus.WORKING
        self.task.start_time = datetime.datetime.now()
        self.task.status = TaskStatus.ACTIVE
        for i, equiment_link in enumerate(self.task_equipment_links):
            equiment_link.equipment.equipStatus = EquipmentStatus.Occupy
        self.session.add_all(self.task_equipment_links)
        self.update_data()
        rospy.loginfo(f"{self.car.name} start to work with the task {self.task.id}!")
        logger.info(f"{self.car.name} start to work with the task {self.task.id}!")

    def update_data(self):
        self.session.add(self.car)
        self.session.add(self.task)
        self.session.commit()
        self.session.refresh(self.car)
        self.session.refresh(self.task)

    def fb_cb(self, fb: TaskListFeedback):
        if self.subTaskStatus != list(fb.task_status):
            self.subTaskStatus = list(fb.task_status)
            for i, equiment_link in enumerate(self.task_equipment_links):
                equiment_link.status = fb.task_status[i]
            self.session.add_all(self.task_equipment_links)
            self.session.commit()
            print(fb)

    def set_goal(self, x_list, y_list, w_list, start_goal):
        self.goalList.task_pose_list.poses.clear()
        self.goalList.task_pose_list.header.stamp = rospy.Time.now()
        o_w_list = []
        o_z_list = []
        for w in w_list:
            q = quaternion_from_euler(0, 0, w)
            o_w_list.append(q[3])
            o_z_list.append(q[2])
        for i in range(len(x_list)):
            pose = Pose()
            pose.orientation.z = o_z_list[i]
            pose.orientation.w = o_w_list[i]
            pose.position.x = x_list[i]
            pose.position.y = y_list[i]
            self.goalList.task_pose_list.poses.append(pose)
        self.goalList.start_goal = start_goal

    def send_goal(self):
        self.client.send_goal(self.goalList, self.done_cb, self.active_cb, self.fb_cb)

    def start_work(self, task: Tasks, car: Cars, session):
        self.reset_data()
        self.session = session
        self.task = task
        self.car = car
        self.user_order = task.UserOrder[0]
        self.task_equipment_links = sorted(task.equipment_links, key=lambda x: x.order)
        x_list = []
        y_list = []
        w_list = []
        task_equipment_links: list[TaskEquipmentLink] = sorted(task.equipment_links, key=lambda x: x.order)
        start_goal = 0
        for i, equiment_link in enumerate(task_equipment_links):
            x_list.append(equiment_link.equipment.x)
            y_list.append(equiment_link.equipment.y)
            w_list.append(equiment_link.equipment.yaw)
            if equiment_link.status == SubTaskStatus.SUCCEEDED:
                start_goal += 1
        if start_goal == len(task_equipment_links):
            task.status = TaskStatus.SUCCEEDED
            self.finished = True
            rospy.logwarn("all gaol has sucess!")
            logger.warning("all gaol has sucess!")
        else:
            self.set_goal(x_list, y_list, w_list, start_goal)
            self.send_goal()
            self.client.wait_for_result()

    def reset_data(self):
        self.session = None
        self.task = None
        self.car = None
        self.user_order = None
        self.finished = False
        self.task_equipment_links = []
        self.subTaskStatus = []


class FastAPiNode():
    def __init__(self) -> None:
        # self.sub = rospy.Subscriber("chatter",String,self.callback,queue_size=10)
        self.CarStatusPub = rospy.Publisher("/dl_agv/cancel", GoalID, queue_size=10)
        self.goalid = GoalID()

    def cancelGoal(self):
        self.CarStatusPub.publish(self.goalid)
    # def callback(self,msg):
    #     self.share_s["data"] = msg.data
    #     rospy.loginfo("I heard:%s",msg.data)

rosNode = FastAPiNode()


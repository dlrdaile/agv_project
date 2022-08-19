import datetime
from typing import Optional

import actionlib
import rospy
from agv_nav.msg import *
from geometry_msgs.msg import Pose
from sensor_msgs.msg import Image
from sqlalchemy import func
from sqlmodel import select
from tf.transformations import quaternion_from_euler
from actionlib_msgs.msg import GoalID
from core.logger import logger
from db.session import Session, get_session
from models.car.car import Cars, CarStatus
from models.car.tasks import Tasks, TaskStatus
from models.item.items import OrderStatus, UserOrder
from models.item.links import TaskEquipmentLink, SubTaskStatus, ItemProcessLink
from models.item.equipment import EquipmentStatus
import tf2_ros
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np



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
            self.task.status = TaskStatus.PAUSE
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
        try:
            for i, equiment_link in enumerate(self.task_equipment_links):
                if state == 2 and result.task_final_status[i] == SubTaskStatus.ACTIVE:
                    equiment_link.status = SubTaskStatus.PAUSE
                else:
                    equiment_link.status = result.task_final_status[i]
                equiment_link.equipment.equipStatus = EquipmentStatus.Free
        except:
            pass
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
                if fb.task_status[i] == TaskStatus.ACTIVE:
                    equiment_link.current_task_iswork = fb.current_task_iswork
                else:
                    equiment_link.current_task_iswork = False
                equiment_link.status = fb.task_status[i]
            self.session.add_all(self.task_equipment_links)
            self.session.commit()
            print(fb)

    def set_goal(self, x_list, y_list, w_list, move_id_set, start_goal):
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
        self.goalList.move_id_set = move_id_set
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
        move_id_set = []
        task_equipment_links: list[TaskEquipmentLink] = sorted(task.equipment_links, key=lambda x: x.order)
        process_item_links: list[ItemProcessLink] = sorted(task.UserOrder[0].item.process_links,
                                                           key=lambda x: x.order)
        start_goal = 0
        for i, equiment_link in enumerate(task_equipment_links):
            x_list.append(equiment_link.equipment.x)
            y_list.append(equiment_link.equipment.y)
            w_list.append(equiment_link.equipment.yaw)
            move_id_set.append(process_item_links[i].process.id)
            if equiment_link.status == SubTaskStatus.SUCCEEDED:
                start_goal += 1
        if start_goal == len(task_equipment_links):
            task.status = TaskStatus.SUCCEEDED
            self.finished = True
            rospy.logwarn("all goal has sucess!")
            logger.warning("all goal has sucess!")

        else:
            self.set_goal(x_list, y_list, w_list, move_id_set, start_goal)
            self.send_goal()
            self.client.wait_for_result()

    def reset_data(self):
        self.goalList = TaskListGoal()
        self.goalList.task_pose_list.header.frame_id = "map"
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
        self.TaskCancelPub = rospy.Publisher("/dl_agv/cancel", GoalID, queue_size=10)
        self.CarTaskStatusPub = rospy.Publisher("/car_task_status", carTaskStatus, queue_size=10)
        self.carStaticPub = rospy.Publisher("/car_task_static", carStaticMsg, queue_size=10)
        self.carTaskStatusTimer = rospy.Timer(rospy.Duration(2), self.TastStatusCallback)
        self.carTaskStaticTimer = rospy.Timer(rospy.Duration(1), self.TastStaticCallback)
        self.demoClient = actionlib.SimpleActionClient("move_set_action", MoveSetAction)
        self.moveset_cancel_pub_ = rospy.Publisher("/move_set_action/cancel", GoalID, queue_size=10)
        self.goalid = GoalID()
        self.buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.buffer)
        self.bridge = CvBridge()

    def cancelGoal(self):
        self.TaskCancelPub.publish(self.goalid)

    def cancelDemoGoal(self):
        self.moveset_cancel_pub_.publish(self.goalid)

    def demoDoneCallback(self, state: actionlib_msgs.msg.GoalStatus, result: MoveSetActionResult):
        with get_session() as session:
            try:
                car: Cars = session.query(Cars).get(1)
                if car.status == CarStatus.WORKING:
                    car.status = CarStatus.FREE
                    session.add(car)
                    session.commit()
            except Exception as e:
                logger.warning(f"demo done run error! because: {e}")

    def callDemo(self, taskId: int):
        started = self.demoClient.wait_for_server(rospy.Duration(1))
        if started:
            goal = MoveSetGoal()
            goal.taskId = taskId
            self.demoClient.send_goal(goal, self.demoDoneCallback)
        return started

    # todo:comlete static
    def TastStaticCallback(self, event):
        with get_session() as session:
            try:
                carTaskStaticData = carStaticMsg()
                carTaskStaticData.current_floor = 1
                car: Cars = session.query(Cars).get(1)
                carTaskStaticData.current_task_id = car.current_task_id if car.current_task_id is not None else -1
                sql = select(Tasks).where(Tasks.status == TaskStatus.WAITING).order_by(Tasks.create_time)
                task = session.exec(sql).first()
                if task is not None:
                    carTaskStaticData.next_task_id = task.id
                else:
                    carTaskStaticData.next_task_id = -1
                sql = select(func.count(Tasks.id)).where(Tasks.status == TaskStatus.SUCCEEDED)
                carTaskStaticData.all_complete_task_num = session.exec(sql).first()
                sql = select(func.count(Tasks.id)).where(Tasks.status == TaskStatus.WAITING)
                carTaskStaticData.ready_task_num = session.exec(sql).first()
                try:
                    trans = self.buffer.lookup_transform("map", "base_footprint", rospy.Time(0))
                    carTaskStaticData.current_x = trans.transform.translation.x
                    carTaskStaticData.current_y = trans.transform.translation.y
                except:
                    carTaskStaticData.current_x = -1
                    carTaskStaticData.current_y = -1
                self.carStaticPub.publish(carTaskStaticData)
            except Exception as e:
                logger.warning(f"the task static pub has something error:{e}")
                pass

    def TastStatusCallback(self, event):
        with get_session() as session:
            try:
                carTaskStatusData = carTaskStatus()
                car: Cars = session.query(Cars).get(1)
                car_status = car.status
                carTaskStatusData.car_status = car_status
                if car.current_task_id is not None:
                    task: Tasks = session.query(Tasks).get(car.current_task_id)
                    if task is not None:
                        task_equipment_links: list[TaskEquipmentLink] = sorted(task.equipment_links,
                                                                               key=lambda x: x.order)
                        process_item_links: list[ItemProcessLink] = sorted(task.UserOrder[0].item.process_links,
                                                                           key=lambda x: x.order)
                        for i, equiment_link in enumerate(task_equipment_links):
                            subtask_desc = SubTaskDesc()
                            subtask_desc.process_name = process_item_links[i].process.name
                            subtask_desc.subtask_status = equiment_link.status
                            subtask_desc.device_id = equiment_link.equipment.name
                            subtask_desc.current_task_iswork = equiment_link.current_task_iswork
                            carTaskStatusData.task_list.append(subtask_desc)
                self.CarTaskStatusPub.publish(carTaskStatusData)
            except Exception as e:
                logger.warning(f"the task status pub has something error:{e}")
                pass

    def callForImage(self):
        try:
            message = rospy.wait_for_message('/camera/left/image_raw', Image, rospy.Duration(5))
        except rospy.exceptions.ROSException as e:
            return None
        try:
            cv_image = self.bridge.imgmsg_to_cv2(message, "bgr8")
        except CvBridgeError as e:
            return None
        return cv_image
        # try:
        #     self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        # except CvBridgeError as e:
        #     print(e)
        # pass


if __name__ == "__main__":
    rospy.init_node("hello")
    rosNode = FastAPiNode()
    while not rospy.is_shutdown():
        rospy.spin()

"""
author:dlr123
date:2022年07月07日
多进程文件
"""
from multiprocessing import Process  # 多进程组件,队列

import rospy
from fastapi import FastAPI
from sqlmodel import select

from core.logger import logger
from core.rosClass import TaskExecutionNode
from db.session import get_session
from models.car.car import Cars, CarStatus
from models.car.tasks import Tasks, TaskStatus


def TaskExecution(name: str, car_name: str):
    rospy.init_node(name)
    taskClient = TaskExecutionNode(name, car_name)
    taskClient.client.wait_for_server()
    wait_rate = rospy.Rate(1)
    relax_rate = rospy.Rate(0.2)
    while not rospy.is_shutdown():
        working = False
        with get_session() as session:
            try:
                car: Cars = session.query(Cars).filter(Cars.name == taskClient.car_name).one()
                if car.status == CarStatus.FREE:
                    if car.current_task_id is not None:
                        task: Tasks = session.query(Tasks).get(car.current_task_id)
                        if task is None:
                            car.current_task_id = None
                            session.add(car)
                            session.commit()
                            raise ValueError("the task is not exit")
                    else:
                        sql = select(Tasks).where(Tasks.status == TaskStatus.WAITING).order_by(Tasks.create_time)
                        task = session.exec(sql).first()
                    if task is not None:
                        working = True
                        car.tasks.append(task)
                        car.current_task_id = task.id
                        session.add(task)
                        session.add(car)
                        session.commit()
                        session.refresh(task)
                        taskClient.start_work(task, car, session)
                        while not taskClient.finished:
                            pass
            except Exception as e:
                session.rollback()
                logger.warning(f"because: {e}")
        if working:
            relax_rate.sleep()
        else:
            wait_rate.sleep()
    rospy.logwarn("the car schedual has been closed!")
    logger.warning("the car schedual has been closed!")


def CreateAgvTask(nodename, agvname):
    task = Process(target=TaskExecution, args=(nodename, agvname), daemon=True)
    return task


def register_process(app: FastAPI):
    app.state.tasks = {}
    app.state.tasks['task1'] = CreateAgvTask("test_action", "dl_agv")
    for task in app.state.tasks.values():
        task.start()


if __name__ == "__main__":
    register_process()

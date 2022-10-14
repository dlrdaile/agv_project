import uvicorn
from fastapi import FastAPI

from core import settings,FastAPiNode
from core.logger import logger
from db import init_db,init_data
from register import register_mount,register_exception,register_cors,register_process,register_middleware,register_router,register_timer
from sqlmodel.sql.expression import Select,SelectOfScalar
import rospy
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
app = FastAPI(description=settings.PROJECT_DESC,version=settings.PROJECT_VERSION)


def create_app() :
    """ 注册中心 """
    register_mount(app)  # 挂载静态文件

    register_exception(app)  # 注册捕获全局异常

    register_router(app)  # 注册路由

    register_middleware(app)  # 注册请求响应拦截

    register_cors(app)  # 注册跨域请求

    register_timer(app)  # 注册定时器

    register_process(app)  #

    logger.info("日志初始化成功！！！")  # 初始化日志


@app.on_event("startup")
async def startup() :
    app.state.engine = init_db()  # 初始化表
    # app.state.engine = init_db(isdrop=True)  # 初始化表
    # await init_data()  # 初始化数据
    rospy.init_node("fastapi_ros")
    app.state.rosnode = FastAPiNode()
    create_app()  # 加载注册中心


@app.on_event("shutdown")
async def shutdown() :
    app.state.sche.shutdown()
    app.state.sche.sche.remove_all_jobs()
    logger.info("系统程序被关闭了")
    await app.state.engine.dispose()  # 关闭 redis


if __name__ == '__main__' :
    # uvicorn.run(app='main:app', host="127.0.0.1", port=8000)
    uvicorn.run(app='main:app',host="0.0.0.0",port=8001)

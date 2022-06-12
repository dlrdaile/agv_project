#
# # this is just to unconfuse pycharm
# try:
#     from cv2 import cv2
# except ImportError:
#     try :
#         import cv2.__init__ as cv2
#     except ImportError :
#         pass
# import uvicorn
# from fastapi import FastAPI,Request
# from fastapi.responses import StreamingResponse
# from fastapi.templating import Jinja2Templates
# camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# app = FastAPI()
# templates = Jinja2Templates(directory=r"D:\Code\WEB\project_dir\agv_project\agv_back_fastapi\test\template")
#
# async def gen_frames() :
#     while True :
#         success,frame = camera.read()
#         if not success :
#             continue
#         else :
#             ret,buffer = cv2.imencode('.jpg',frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
#
# @app.get('/')
# def index(request: Request) :
#     return templates.TemplateResponse("index.html",{"request" : request})
#
#
# @app.get('/video_feed')
# async def video_feed() :
#     return StreamingResponse(gen_frames(),media_type='multipart/x-mixed-replace; boundary=frame')
#
# @app.get('/close')
# async def close_video():
#     camera.release()
# if __name__ == '__main__' :
#     uvicorn.run(app,host='127.0.0.1',port=8000,debug=True)
import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI,Request,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path

from starlette.responses import StreamingResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=("*",),
    allow_headers=("*",),
)


# camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# templates = Jinja2Templates(directory=r"D:\Code\WEB\project_dir\agv_project\agv_back_fastapi\test\template")
#
#
# @app.get('/')
# def index(request: Request) :
#     return templates.TemplateResponse("index.html",{"request" : request})
#
#
# @app.websocket("/ws")
# async def get_stream(websocket: WebSocket) :
#     await websocket.accept()
#     try :
#         while True :
#             success,frame = camera.read()
#             if not success :
#                 break
#             else :
#                 ret,buffer = cv2.imencode('.jpg',frame)
#                 await websocket.send_bytes(buffer.tobytes())
#     except WebSocketDisconnect :
#         print("Client disconnected")
class MyData(BaseModel) :
    hello: str


@app.post('/uploadfiles/')
async def get_upload_url(*,uploadFiles: list[UploadFile],req: Request) :
    content = uploadFiles[0].file.read()
    filepath = Path(uploadFiles[0].filename)
    img = cv2.imdecode(np.frombuffer(content,np.uint8),cv2.IMREAD_COLOR)
    if not filepath.exists():
        filepath.write_bytes(content)
    ret,buffer = cv2.imencode(filepath.suffix,img)
    frame = buffer.tobytes()
    # def iter():
    #     yield from (b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # return StreamingResponse(iter(),media_type='multipart/x-mixed-replace; boundary=frame')
    return {'code':200}


@app.options('/uploadfiles/')
def justify() :
    return HTMLResponse(status_code=200)


if __name__ == '__main__' :
    uvicorn.run('main_test:app',host='127.0.0.1',port=8000,reload=True)

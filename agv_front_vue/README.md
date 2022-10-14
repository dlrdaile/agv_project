# **agv_front_vue**

> 这是agv调度软件的前端部分

## 构建项目

> 项目基于[vue-admin-template](https://github.com/PanJiaChen/vue-admin-template)开发

本项目主要使用以下工具：

* node(v16.13.2)
* vue2、vuex、vue-route、axios
* element-ui
* datav
* Echart

```bash
# 克隆项目
# git clone https://github.com/dlrdaile/agv_project.git
# 确保已经clone或下载项目到本地
# 进入项目目录
cd agv_project/agv_front_vue/

# 安装依赖
npm install

# 建议不要直接使用 cnpm 安装以来，会有各种诡异的 bug。可以通过如下操作解决 npm 下载速度慢的问题
npm install --registry=https://registry.npm.taobao.org
```

## 修改后端服务IP

1. 打开`.env.development`文件，将其中的IP地址修改为您当前电脑的IP地址，或者更改为localhost(这样将无法在其他设备上访问该网页)

## 运行项目

> 注意这样只能进入登陆界面而无法访问网页内容，若想访问网页内容，请先启动后端程序

```bash
npm run dev
```

----

**返回[`Install.md`](../Install.md)**

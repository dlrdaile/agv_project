<template>
  <div class="main-container" style="margin:0">
    <div class="task fill">
      <dv-decoration-7 style="width:150px;height:30px;position: relative;left: 26%;color: whitesmoke">任务序列
      </dv-decoration-7>
      <div class="taskMain" style="position:relative;height: 100%">
        <dv-scroll-board :config="config" class="fill" />
      </div>
    </div>
    <div class="history">
      <div class="digital-flop">
        <div
          v-for="item in digitalFlopDataUp"
          :key="item.title"
          class="digital-flop-item"
        >
          <div class="digital-flop-title">{{ item.title }}</div>
          <div class="digital-flop">
            <dv-digital-flop
              :config="item.number"
              style="width:60px;height:50px;"
            />
            <div class="unit">{{ item.unit }}</div>
          </div>
        </div>
      </div>
      <div class="digital-flop">
        <div
          v-for="item in digitalFlopDataBelow"
          :key="item.title"
          class="digital-flop-item"
        >
          <div class="digital-flop-title">{{ item.title }}</div>
          <div class="digital-flop">
            <dv-digital-flop
              :config="item.number"
            />
            <div class="unit">{{ item.unit }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="logger">
      <el-table
        border
        :data="sensorStatusData"
        height="100%"
        style="width: 100%;height: 100%;position: absolute"
        :cell-style="TableCellStyle"
      >
        <el-table-column
          prop="imgPath"
          label="实体"
          align="center"
          min-width="120"
        >
          <template v-slot="scope">
            <el-image
              style="width: 60px; height: 40px"
              :src="scope.row.imgPath"
              :preview-src-list="[scope.row.imgPath]"
            >
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline" />
              </div>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column
          prop="name"
          label="类型"
          align="center"
        />
        <el-table-column
          prop="status"
          label="状态"
          align="center"
        >
          <template v-slot="scope">
            <el-switch
              v-model="scope.row.status"
              active-color="#13ce66"
              inactive-color="#ff4949"
              disabled
            />
          </template>

        </el-table-column>
      </el-table>
    </div>
    <dv-border-box-8 class="model">
      <ros-scene-area
        :rosview-object="rosviewObject"
        :ros="ros"
        :connected="connected"
      />
    </dv-border-box-8>
    <div class="panel fill">
      <div class="xspeed fill">
        <speed-chart
          :data-arr="xspeed"
          :vmax="max_vel_x"
          class="fill"
          :title="xSpeedTitle"
          :format-function="xSpeedFormatFunction"
        />
      </div>
      <div class="yspeed fill">
        <speed-chart
          :data-arr="yspeed"
          :vmax="max_vel_y"
          :title="ySpeedTitle"
          class="fill"
        />
      </div>
      <div class="wspeed fill">
        <speed-chart
          :data-arr="wspeed"
          :vmax="max_vel_theta"
          :title="wSpeedTitle"
          class="fill"
        />
      </div>
      <div class="press fill">
        <press-chart
          :vmax="max_press"
          :value="pressValue"
          class="fill"
        />
      </div>
    </div>

    <div class="camera fill">
      <split-pane split="vertical" :min-percent="30" :default-percent="50">
        <template slot="paneL">
          <img :src="leftCameraSrc" class="fill">
        </template>
        <template slot="paneR">
          <img :src="rightCameraSrc" class="fill">
        </template>
      </split-pane>
    </div>
    <div class="status">
      <el-select v-model="seletParamName" placeholder="ros_param" @focus="getParamInfo">
        <el-option
          v-for="(item,index) in rosParam"
          :key="index"
          :label="item"
          :value="item"
        />
      </el-select>
    </div>
    <div class="control">
      <ros-key-cmd
        :ros="ros"
        :acc_lim_theta="acc_lim_theta"
        :acc_lim_x="acc_lim_x"
        :acc_lim_y="acc_lim_y"
        :max_vel_theta="max_vel_theta"
        :max_vel_x="max_vel_x"
        :max_vel_y="max_vel_y"
        :topic-name="cmdVelTopicName"
      />
    </div>

  </div>
</template>

<script>
import rosSceneArea from '@/views/rosPanel/component/MainBodyComponent/RosSceneArea'
import RosKeyCmd from '@/components/rosCompoent/RosCtrl/RosKeyCmd'
import Nipple from '@/components/rosCompoent/RosCtrl/Nipple'
import splitPane from 'vue-splitpane'
import SpeedChart from '@/views/rosPanel/component/MainBodyComponent/SpeedChart'
import PressChart from '@/views/rosPanel/component/MainBodyComponent/PressChart'

export default {
  name: 'MainBody',
  components: {
    rosSceneArea,
    RosKeyCmd,
    Nipple,
    splitPane,
    SpeedChart,
    PressChart
  },
  props: {
    connected: {
      type: Boolean,
      default: false
    },
    ros: {
      type: Object,
      default: null,
      require: true
    }
  },
  data() {
    return {
      speed: 3,
      vmax: 10,
      rosviewObject: {
        position: 'absolute',
        width: '95%',
        height: '95%',
        left: '49%',
        top: '50%',
        transform: 'translate(-50%, -50%)'
      },
      rosParam: [],
      myChart: null,
      rightCameraSrc: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
      leftCameraSrc: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
      cameraRight: null,
      cameraLeft: null,
      sensorStatus: null,
      TaskStatus: null,
      TaskStatic: null,
      acc_lim_theta: Math.PI / 10,
      acc_lim_x: 0.1,
      acc_lim_y: 0.1,
      max_vel_theta: Math.PI / 2,
      max_vel_x: 0.5,
      max_vel_y: 0.5,
      cmdVelTopic: null,
      cmdVelTopicName: '/cmd_vel',
      wspeed: 0,
      xspeed: 0,
      yspeed: 0,
      xSpeedTitle: 'x方向',
      ySpeedTitle: 'y方向',
      wSpeedTitle: 'z转轴',
      max_press: 5,
      pressValue: 1,
      seletParamName: null,
      sensorStatusData: [{
        imgPath: this.$localUrl + '/static/img/sensor_image/odom.png',
        name: '里程计',
        status: true
      }, {
        imgPath: this.$localUrl + '/static/img/sensor_image/laser.png',
        name: '雷达',
        status: false
      }, {
        imgPath: this.$localUrl + '/static/img/sensor_image/zed-2-front.jpg',
        name: '双目相机',
        status: false
      }, {
        imgPath: this.$localUrl + '/static/img/sensor_image/press.png',
        name: '压力计',
        status: false
      }, {
        imgPath: this.$localUrl + '/static/img/sensor_image/imu.jpg',
        name: '惯性导航仪',
        status: false
      }],
      batteryIsOpen: false,
      digitalFlopDataUp: [],
      digitalFlopDataBelow: [],
      config: {
        header: ['工艺', '作业设备', '当前状态'],
        data: [],
        index: true,
        columnWidth: [40, 60, 100],
        align: ['center']
      },
      defaultTaskStatusData: [
        ['<span style="color:#37a2da;">行1列1</span>', '行1列2', '行1列3'],
        ['行2列1', '<span style="color:#32c5e9;">行2列2</span>', '行2列3'],
        ['行3列1', '行3列2', '<span style="color:#67e0e3;">行3列3</span>'],
        ['行4列1', '<span style="color:#9fe6b8;">行4列2</span>', '行4列3']
      ],
      carXPosition: 0,
      carYPosition: 0,
      currentTaskID: -1,
      nextTaskID: -1,
      completeTaskNum: 0,
      readyTaskNum: 0,
      oneDay: 24 * 3600 * 1000,
      value: Math.random() * 1000,
      now: new Date(1997, 9, 3),
      chartData: [],
      timeId: null
    }
  },
  mounted() {
    var that = this
    this.create_chart()
    this.timeId = setInterval(function() {
      for (var i = 0; i < 5; i++) {
        that.chartData.shift()
        that.chartData.push(that.randomData())
      }
      that.myChart.setOption({
        series: [
          {
            data: that.chartData
          }
        ]
      })
    }, 1000)
    this.cameraRight = new ROSLIB.Topic({
      ros: this.ros,
      name: '/camera/right/image_raw/compressed',
      compression: 'png',
      messageType: 'sensor_msgs/CompressedImage',
      queue_length: 1,
      throttle_rate: 20
    })
    this.cameraLeft = new ROSLIB.Topic({
      ros: this.ros,
      name: '/camera/left/image_raw/compressed',
      compression: 'png',
      messageType: 'sensor_msgs/CompressedImage',
      queue_length: 1,
      throttle_rate: 20
    })
    this.sensorStatus = new ROSLIB.Topic({
      ros: this.ros,
      name: '/sensor_status',
      messageType: 'agv_nav/useSensorStatus'
    })
    this.cmdVelTopic = new ROSLIB.Topic({
      ros: this.ros,
      name: this.cmdVelTopicName,
      messageType: 'geometry_msgs/Twist'
    })
    this.TaskStatus = new ROSLIB.Topic({
      ros: this.ros,
      name: '/car_task_status',
      messageType: 'agv_nav/carTaskStatus'
    })
    this.TaskStatic = new ROSLIB.Topic({
      ros: this.ros,
      name: '/car_task_static',
      messageType: 'agv_nav/carStaticMsg'
    })
    // Then we add a callback to be called every time a message is published on this topic.
    this.cameraRight.subscribe(this.receiveRightImage)
    this.cameraLeft.subscribe(this.receiveLeftImage)
    this.cmdVelTopic.subscribe(this.receiveCmdVelMessage)
    this.sensorStatus.subscribe(this.receiveSensorStatus)
    this.TaskStatus.subscribe(this.receiveTaskStatus)
    this.TaskStatic.subscribe(this.receiveTaskStatic)
    this.config.data = this.defaultTaskStatusData
  },
  beforeDestroy() {
    if (this.cameraRight !== null) {
      this.cameraRight.unsubscribe(this.receiveRightImage)
    }
    if (this.cameraLeft !== null) {
      this.cameraLeft.unsubscribe(this.receiveLeftImage)
    }
    if (this.cmdVelTopic !== null) {
      this.cmdVelTopic.unsubscribe(this.receiveCmdVelMessage)
    }
    if (this.sensorStatus !== null) {
      this.sensorStatus.unsubscribe(this.receiveSensorStatus)
    }
    if (this.TaskStatus !== null) {
      this.TaskStatus.unsubscribe(this.receiveTaskStatus)
    }
    if (this.TaskStatic !== null) {
      this.TaskStatic.unsubscribe(this.receiveTaskStatic)
    }
    if (this.timeId !== null) {
      clearInterval(this.timeId)
    }
  },
  methods: {
    randomData() {
      this.now = new Date(+this.now + this.oneDay)
      this.value = this.value + Math.random() * 21 - 10
      return {
        name: this.now.toString(),
        value: [
          [this.now.getFullYear(), this.now.getMonth() + 1, this.now.getDate()].join('/'),
          Math.round(this.value)
        ]
      }
    },
    createData() {
      this.digitalFlopDataUp = [
        {
          title: '已完成任务',
          number: {
            number: [this.completeTaskNum],
            content: '{nt}',
            style: {
              fill: '#4d99fc',
              fontWeight: 'bold'
            }
          },
          unit: '个'
        },
        {
          title: '当前任务号',
          number: {
            number: [this.currentTaskID],
            content: '{nt}',
            style: {
              fill: '#f46827',
              fontWeight: 'bold'
            }
          }
        },
        {
          title: '当前楼层',
          number: {
            number: [1],
            content: '{nt}',
            textAlign: 'right',
            style: {
              fill: '#40faee',
              fontWeight: 'bold'
            }
          },
          unit: '层'
        }
      ]
      this.digitalFlopDataBelow = [
        {
          title: '待完成任务',
          number: {
            number: [this.readyTaskNum],
            content: '{nt}',
            style: {
              fill: '#4d99fc',
              fontWeight: 'bold'
            }
          },
          unit: '个'
        },
        {
          title: '下一任务号',
          number: {
            number: [this.nextTaskID],
            content: '{nt}',
            style: {
              fill: '#f46827',
              fontWeight: 'bold'
            }
          }
        },
        {
          title: '当前坐标',
          number: {
            number: [this.carXPosition, this.carXPosition],
            content: '({nt},{nt})',
            toFixed: 2,
            style: {
              fill: '#40faee',
              fontWeight: 'bold',
              fontSize: 13
            }
          }
        }
      ]
    },
    receiveSensorStatus(message) {
      this.sensorStatusData.forEach((item) => {
        switch (item.name) {
          case '里程计':
            item.status = message.use_odom
            break
          case '雷达':
            item.status = message.use_laser
            break
          case '双目相机':
            item.status = message.use_camera
            break
          case '惯性导航仪':
            item.status = message.use_imu
            break
          case '压力计':
            item.status = message.use_press
            break
          default:
            break
        }
        this.$bus.$emit('batteryStatus', message.use_battery)
      })
    },
    receiveCmdVelMessage(message) {
      this.xspeed = Math.abs(message.linear.x)
      this.yspeed = Math.abs(message.linear.y)
      this.wspeed = Math.abs(message.angular.z)
      if (message.linear.x > 0) {
        this.xSpeedTitle = '+x方向(前进)'
      } else if (message.linear.x === 0) {
        this.xSpeedTitle = 'x方向'
      } else {
        this.xSpeedTitle = '-x方向(后退)'
      }
      if (message.linear.y > 0) {
        this.ySpeedTitle = '+y方向(左移)'
      } else if (message.linear.y === 0) {
        this.ySpeedTitle = 'y方向'
      } else {
        this.ySpeedTitle = '-y方向(右移)'
      }
      if (message.angular.z > 0) {
        this.wSpeedTitle = '+z转轴(逆时针)'
      } else if (message.angular.z === 0) {
        this.wSpeedTitle = 'z转轴'
      } else {
        this.wSpeedTitle = '-z转轴(顺时针)'
      }
    },
    receiveRightImage(message) {
      // console.log('Received message on ' + listener.name + ': ' + message.data);
      this.rightCameraSrc = 'data:image/jpg;base64,' + message.data
      // console.log(message);
      // If desired, we can unsubscribe from the topic as well.
      // this.unsubscribe();
    },
    receiveLeftImage(message) {
      // console.log('Received message on ' + listener.name + ': ' + message.data);
      this.leftCameraSrc = 'data:image/jpg;base64,' + message.data
      // console.log(message);
      // If desired, we can unsubscribe from the topic as well.
      // this.unsubscribe();
    },
    create_chart() {
      const status = document.querySelector('.status')
      for (var i = 0; i < 1000; i++) {
        this.chartData.push(this.randomData())
      }
      this.myChart = this.$echarts.init(status)
      window.onresize = this.myChart.resize
      const option = {
        title: {
          text: 'Dynamic Data & Time Axis'
        },
        tooltip: {
          trigger: 'axis',
          formatter: function(params) {
            params = params[0]
            var date = new Date(params.name)
            return (
              date.getDate() +
              '/' +
              (date.getMonth() + 1) +
              '/' +
              date.getFullYear() +
              ' : ' +
              params.value[1]
            )
          },
          axisPointer: {
            animation: false
          }
        },
        xAxis: {
          type: 'time',
          splitLine: {
            show: false
          }
        },
        yAxis: {
          type: 'value',
          boundaryGap: [0, '100%'],
          splitLine: {
            show: false
          }
        },
        series: [
          {
            name: 'Fake Data',
            type: 'line',
            showSymbol: false,
            data: this.chartData
          }
        ]
      }
      this.myChart.setOption(option)
    },
    xSpeedFormatFunction(value) {
      return parseFloat(value).toFixed(2)
    },
    ySpeedFormatFunction(value) {
      return parseFloat(value).toFixed(2)
    },
    wSpeedFormatFunction(value) {
      return parseFloat(value).toFixed(2)
    },
    getparam() {
      // Getting a param value
      // ---------------------
      var that = this
      var favoriteColor = new ROSLIB.Param({
        ros: this.ros,
        name: this.seletParamName
      })

      favoriteColor.get(function(value) {
        console.log(`My robot\'s ${that.seletParamName} is ` + value)
      })
    },
    getParamInfo() {
      var that = this
      that.rosParam = {}
      this.ros.getParams(result => {
        that.rosParam = result
      }, error => {
        console.log('getParams error,because', error)
      })
    },
    TableCellStyle(row, column, rowIndex, columnIndex) {
      var cell_style = {}
      if (columnIndex === 0) {
        cell_style['padding'] = '1px'
      }
      cell_style['background-color'] = 'rgba(82,125,151,0.1)'
      return cell_style
    },
    receiveTaskStatus(msg) {
      this.$bus.$emit('carStatus', msg.car_status)
      if (!(msg.car_status !== 2 || msg.car_status !== 3)) {
        this.config.data = this.defaultTaskStatusData
      } else {
        this.config.data = msg.task_list.map((item) => {
          var status_name = ''
          switch (item.subtask_status) {
            case 0:
              status_name = '等待作业'
              break
            case 1:
              status_name = item.subtask_status.current_task_iswork ? '正在加工' : '前往工位'
              break
            case 2:
              status_name = '完成作业'
              break
            case 3:
              status_name = '作业失败'
              break
            case 4:
              status_name = '暂停作业'
              break
            default:
              break
          }
          return [item.process_name, item.device_id, status_name]
        })
      }
      this.config = { ...this.config } // 用以使datav变化
    },
    receiveTaskStatic(msg) {
      this.carXPosition = msg.current_x
      this.carYPosition = msg.current_y
      this.readyTaskNum = msg.ready_task_num
      this.completeTaskNum = msg.all_complete_task_num
      this.currentTaskID = msg.current_task_id
      this.nextTaskID = msg.next_task_id
      this.createData()
    }
  }
}
</script>

<style lang="scss" scoped>
.main-container {
  display: grid;
  position: absolute;
  grid-template-columns: 0.7fr 1.5fr 0.8fr;
  grid-template-rows: 0.9fr 1.2fr 0.9fr;
  gap: 10px 10px;
  grid-auto-flow: row;
  grid-template-areas:
    "task model camera"
    "history model status"
    "logger panel control";
}

.task {
  position: absolute;
  grid-area: task;

  .taskMain {
    display: grid;
    grid-area: taskMain;
  }
}

.history {
  grid-area: history;
  position: absolute;
  width: 100%;
  height: 100%;

  .digital-flop {
    position: relative;
    height: 50%;
    flex-shrink: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: rgba(6, 30, 93, 0.5);

    .digital-flop-item {
      width: 30%;
      height: 70%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-left: 3px solid rgb(6, 30, 93);
      border-right: 3px solid rgb(6, 30, 93);
    }

    .digital-flop-title {
      font-size: 16px;
      color: #a76b6b;
      margin-bottom: 8px;
    }

    .digital-flop {
      display: flex;
    }

    .unit {
      color: white;
      margin-left: 5px;
      font-size: 18px;
      display: flex;
      align-items: flex-end;
      box-sizing: border-box;
      padding-bottom: 3px;
    }
  }
}

::v-deep.logger {
  grid-area: logger;
  position: absolute;
  width: 100%;
  height: 100%;

  .el-table .el-table__cell {
    padding: 1px;
    padding-top: 9px;
  }

  .el-table__body-wrapper {
    height: 200px; /* ¹ö¶¯ÌõÕûÌå¸ß ±ØÐëÏî */
    border-right: none;
    overflow-y: scroll; /* overflow-yÎªÁË²»³öÏÖË®Æ½¹ö¶¯Ìõ*/
  }

  .el-table__body-wrapper::-webkit-scrollbar {
    width: 5px; /* ¹ö¶¯ÌõµÄ¿í¸ß ±ØÐëÏî */
    height: 5px;
  }

  .el-table__body-wrapper::-webkit-scrollbar-thumb {
    background-color: #bfcbd9; /* ¹ö¶¯ÌõµÄ¿í */
    border-radius: 3px;
  }

  .el-table th {
    background: rgba(1, 11, 30, 0.2);

    .gutter {
      width: 2px;
    }
  }

  .el-table thead {
    color: #d2d8e1;
    font-weight: 500;
  }

  .el-table {
    color: #e1d9d9;
    font-size: 14px;
  }

  .el-table td, .building-top .el-table th.is-leaf {
    border-bottom: 1px solid #d2d8e1;
  }

  .el-table tr {
    background: rgb(7, 14, 31);
  }
}

.model {
  grid-area: model;
  position: absolute;
  width: 100%;
  height: 100%;
}

.panel {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: 1fr;
  gap: 0px 0px;
  grid-template-areas:
    "xspeed yspeed wspeed press";
  grid-area: panel;
}

.xspeed {
  grid-area: xspeed;
}

.yspeed {
  grid-area: yspeed;
}

.wspeed {
  grid-area: wspeed;
}

.press {
  grid-area: press;
}

.camera {
  grid-area: camera;

  .camera-content {
    position: absolute;
    width: 95%;
    height: 95%;
    left: 2%;
    top: 2.5%;
  }

  img {
    padding: 2px;
  }
}

.status {
  grid-area: status;
}

.control {
  position: absolute;
  width: 100%;
  height: 100%;
  grid-area: control;
}

.fill {
  position: absolute;
  width: 100%;
  height: 100%;
}
</style>

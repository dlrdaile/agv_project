<template>
  <div class="main-container" style="margin:0">
    <div class="task">
      <dv-decoration-7 style="width:150px;height:30px;position: absolute;left: 27%;color: pink">任务序列</dv-decoration-7>
      <div style="width: 50px;height: 50px;background-color: #4AB7BD;position: absolute" />
    </div>
    <div class="history" />
    <div class="logger" />
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
    <div class="status" />
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
      myChart: null,
      rightCameraSrc: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
      leftCameraSrc: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
      cameraRight: null,
      cameraLeft: null,
      acc_lim_theta: Math.PI / 10,
      acc_lim_x: 0.1,
      acc_lim_y: 0.5,
      max_vel_theta: Math.PI / 2,
      max_vel_x: 1.0,
      max_vel_y: 1.0,
      cmdVelTopic: null,
      cmdVelTopicName: '/cmd_vel',
      wspeed: 0,
      xspeed: 0,
      yspeed: 0,
      xSpeedTitle: 'x方向',
      ySpeedTitle: 'y方向',
      wSpeedTitle: 'z转轴',
      max_press: 5,
      pressValue: 1
    }
  },
  mounted() {
    this.create_chart()
    this.cameraRight = new ROSLIB.Topic({
      ros: this.ros,
      name: '/multisense_sl/camera/right/image_raw/compressed',
      compression: 'png',
      messageType: 'sensor_msgs/CompressedImage',
      queue_length: 1,
      throttle_rate: 20
    })
    this.cameraLeft = new ROSLIB.Topic({
      ros: this.ros,
      name: '/multisense_sl/camera/left/image_raw/compressed',
      compression: 'png',
      messageType: 'sensor_msgs/CompressedImage',
      queue_length: 1,
      throttle_rate: 20
    })
    this.cmdVelTopic = new ROSLIB.Topic({
      ros: this.ros,
      name: this.cmdVelTopicName,
      messageType: 'geometry_msgs/Twist'
    })
    // Then we add a callback to be called every time a message is published on this topic.
    this.cameraRight.subscribe(this.receiveRightImage)
    this.cameraLeft.subscribe(this.receiveLeftImage)
    this.cmdVelTopic.subscribe(this.receiveCmdVelMessage)
  },
  beforeDestroy() {
    if (this.cameraRight !== null) {
      this.cameraRight.unsubscribe(this.cameraRight)
    }
    if (this.cameraLeft !== null) {
      this.cameraLeft.unsubscribe(this.cameraLeft)
    }
  },
  methods: {
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
      this.myChart = this.$echarts.init(status)
      window.onresize = this.myChart.resize
      this.myChart.setOption({
        title: {
          text: 'ECharts 入门示例'
        },
        tooltip: {},
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        },
        yAxis: {},
        series: [
          {
            name: '销量',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
          }
        ]
      })
    },
    xSpeedFormatFunction(value) {
      return parseFloat(value).toFixed(2)
    },
    ySpeedFormatFunction(value) {
      return parseFloat(value).toFixed(2)
    },
    wSpeedFormatFunction(value) {
      return parseFloat(value).toFixed(2)
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
}

.history {
  background-color: pink;
  grid-area: history;
}

.logger {
  background-color: pink;
  grid-area: logger;
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
  .camera-content{
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

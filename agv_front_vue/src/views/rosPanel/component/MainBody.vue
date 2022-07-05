<template>
  <div class="main-container" style="margin:0">
    <dv-border-box-10 class="task">
      <dv-decoration-7 style="width:150px;height:30px;position: absolute;left: 27%;color: pink">任务序列</dv-decoration-7>
      <div style="width: 50px;height: 50px;background-color: #4AB7BD;position: absolute" />
    </dv-border-box-10>
    <div class="history" />
    <div class="logger" />
    <dv-border-box-8 class="model">
      <ros-scene-area
        :rosview-object="rosviewObject"
        :ros="ros"
        :connected="connected"
      />
    </dv-border-box-8>
    <!--    <div class="model">-->
    <!--      <ros-scene-area-->
    <!--        :rosview-object="rosviewObject"-->
    <!--      />-->
    <!--    </div>-->
    <div class="panel fill">
      <div class="xspeed fill">
        <speed-chart
          :data-arr="speed"
          :vmax="vmax"
          class="fill"
        />
      </div>
      <div class="yspeed fill">
        <speed-chart
          :data-arr="speed"
          :vmax="vmax"
          class="fill"
        />
      </div>
      <div class="wspeed fill">
        <speed-chart
          :data-arr="speed"
          :vmax="vmax"
          class="fill"
        />
      </div>
      <div class="press" />

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
export default {
  name: 'MainBody',
  components: {
    rosSceneArea,
    RosKeyCmd,
    Nipple,
    splitPane,
    SpeedChart
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
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)'
      },
      myChart: null,
      rightCameraSrc: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
      leftCameraSrc: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
      cameraRight: null,
      cameraLeft: null
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

    // Then we add a callback to be called every time a message is published on this topic.
    // this.cameraRight.subscribe(this.receiveRightImage)
    // this.cameraLeft.subscribe(this.receiveLeftImage)
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
    }
  }
}
</script>

<style lang="scss" scoped>
.main-container {  display: grid;
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
  grid-area: task;}

.history {
  background-color: pink;
  grid-area: history; }

.logger {
  background-color: pink;
  grid-area: logger; }

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

.xspeed { grid-area: xspeed; }
.yspeed { grid-area: yspeed; }
.wspeed { grid-area: wspeed; }
.press { grid-area: press; }

.camera {
  grid-area: camera;
  img {
    padding: 2px;
  }
}

.status {
  grid-area: status; }

.control {
  position: absolute;
  width: 100%;
  height: 100%;
  grid-area: control;}
.fill {
  position: absolute;
  width: 100%;
  height: 100%;
}
</style>

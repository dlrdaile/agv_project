<template>
  <div class="keycmd-container">
    <button
      @keydown.stop="handleKeyDown($event)"
      @keyup.stop="handleKeyUp($event)"
    >
      键盘控制区
    </button>
  </div>
</template>

<script>
import KEYBOARDTELEOP from '@/utils/teleop.js'
export default {
  props: {
    max_vel_x: {
      require: false,
      default: 1.0,
      type: Number
    },
    max_vel_y: {
      require: false,
      default: 1.0,
      type: Number
    },
    max_vel_theta: {
      require: false,
      default: Math.PI / 2,
      type: Number
    },
    acc_lim_x: {
      require: false,
      default: 0.1,
      type: Number
    },
    acc_lim_y: {
      require: false,
      default: 0.5,
      type: Number
    },
    acc_lim_theta: {
      require: false,
      default: Math.PI / 10,
      type: Number
    },
    init_x: {
      require: false,
      default: 0,
      type: Number
    },
    init_y: {
      require: false,
      default: 0,
      type: Number
    },
    init_theta: {
      require: false,
      default: 0,
      type: Number
    },
    topicName: {
      require: false,
      default: '/cmd_vel',
      type: String
    }
    // initros:{
    //   require:true
    // }
  },
  data() {
    return {
      teleop: () => {}
      // ros:this.initros
    }
  },
  created() {
    this.teleop = new KEYBOARDTELEOP({
      ros: this.$parent.ros,
      topic: this.topicName,
      max_vel_x: this.max_vel_x,
      max_vel_y: this.max_vel_y,
      max_vel_theta: this.max_vel_theta,
      acc_lim_theta: this.acc_lim_theta,
      acc_lim_x: this.acc_lim_x,
      acc_lim_y: this.acc_lim_y,
      init_theta: this.init_theta,
      init_x: this.init_x,
      init_y: this.init_y
    })
  },
  methods: {
    handleKeyDown(e) {
      this.teleop.handleKeyDown(e)
    },
    handleKeyUp(e) {
      this.teleop.handleKeyUp(e)
    }
  }
}
</script>

<style lang="scss" scoped>
.keycmd-container {
  background-color: pink;
  // position: absolute;
  button {
    width: 300px;
    height: 500px;
  }
}
</style>

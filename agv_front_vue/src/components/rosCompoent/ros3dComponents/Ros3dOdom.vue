<template>
  <div class="odom-container" />
</template>

<script>
export default {
  name: 'Ros3dOdom',
  props: {
    topic: {
      type: String,
      require: false,
      default: '/odom'
    },
    keep: {
      type: Number,
      require: false,
      default: 1
    },
    color: {
      type: [Number, String],
      require: false,
      default: 0xcc00ff
    },
    length: {
      type: Number,
      require: false,
      default: 1.0
    },
    headLength: {
      type: Number,
      require: false,
      default: 0.2
    },
    shaftDiameter: {
      type: Number,
      require: false,
      default: 0.05
    },
    headDiameter: {
      type: Number,
      require: false,
      default: 0.1
    }
  },
  data() {
    return {
      object: null
    }
  },
  mounted() {
    this.createObject()
  },
  beforeDestroy() {
    for (let i = 0; i < this.object.sns.length; i++) {
      this.sns[i].unsubscribeTf()
      this.rootObject.remove(this.sns[i])
      this.sns.shift()
    }
  },
  methods: {
    createObject() {
      this.object = new ROS3D.Odometry({
        topic: this.topic,
        ros: this.$parent.ros,
        tfClient: this.$parent.tfClient,
        rootObject: this.$parent.viewer.scene,
        keep: this.keep,
        color: this.color,
        length: this.length,
        headLength: this.headLength,
        shaftDiameter: this.shaftDiameter,
        headDiameter: this.headDiameter
      })
      this.object.name = this._uid
    }
  }
}
</script>

<style>
</style>

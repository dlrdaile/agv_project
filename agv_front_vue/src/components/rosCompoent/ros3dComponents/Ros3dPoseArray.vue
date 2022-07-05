<template>
  <div class="pose-array-container" />
</template>

<script>
export default {
  name: 'Ros3dPoseArray',
  props: {
    topic: {
      type: String,
      require: true
    },
    color: {
      type: [Number, String],
      require: false,
      default: '#256fab'
    },
    length: {
      type: Number,
      require: false,
      default: 0.5
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
    if (this.object.sn !== null) {
      this.object.sn.unsubscribeTf()
      this.$parent.viewer.scene.remove(this.object.sn)
      this.object.unsubscribe()
    }
  },
  methods: {
    createObject() {
      this.object = new ROS3D.PoseArray({
        ros: this.$parent.ros,
        tfClient: this.$parent.tfClient,
        rootObject: this.$parent.viewer.scene,
        topic: this.topic,
        color: this.color,
        length: this.length
      })
    }
  }
}
</script>

<style>
</style>

<template>
  <div class="pose-with-covariance-container" />
</template>

<script>
export default {
  name: 'Ros3dPoseWithCovariance',
  props: {
    topic: {
      type: String,
      require: true
    },
    color: {
      type: [Number, String],
      require: false,
      default: '#9925ab'
    }
  },
  data() {
    return {
      object: null
    }
  },
  watch: {
    topic(n) {
      this.object.unsubscribe()
      this.object.topicName = n
      this.object.subscribe()
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
        color: this.color
      })
    }
  }
}
</script>

<style>
</style>

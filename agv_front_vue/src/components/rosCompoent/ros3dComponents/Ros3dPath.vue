<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

/**
 * A Path client that listens to a given topic and displays a line connecting the poses.
 * It is a wrapper for [`ROS3D.Path`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Path.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {String} [topic=] - The path topic to listen to
 * @vue-prop {String} [color=#009688] - The color to use for this arrow
 *
 * @vue-data {ROS3D.Path} object - Handle for the internal [ROS3D.Path]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Path.html}
 */
export default {
  name: 'Ros3dPath',
  props: {
    topic: {
      type: String,
      default: '',
      require: false
    },
    color: {
      type: String,
      default: '#009688',
      require: false
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
      this.object = new ROS3D.Path({
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

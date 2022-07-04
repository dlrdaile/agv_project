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
    visible: {
      type: Boolean,
      default: true,
      require: false
    },
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
    },
    color(n) {
      this.object.color = n
    },
    visible(newState) {
      if (newState) this.show()
      else this.hide()
    }
  },
  mounted() {
    this.object = new ROS3D.Path({
      ros: this.$parent.ros,
      tfClient: this.$parent.tfClient,
      rootObject: this.$parent.viewer.scene,
      topic: this.topic,
      color: this.color
    })
    this.object.name = this._uid
    if (!this.visible) this.hide()
  },
  beforeDestroy() {
    this.object.unsubscribe()
    this.hide()
  },
  methods: {
    show() {
      this.$parent.viewer.scene.add(this.object)
    },
    hide() {
      var obj = this.$parent.viewer.scene.getObjectByName(this._uid)
      if (obj != null) this.$parent.viewer.scene.remove(obj)
    }
  }
}
</script>

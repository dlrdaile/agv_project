<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

/**
 * A client for an interactive marker topic.
 * It is a wrapper for [`ROS3D.InteractiveMarkerClient`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.InteractiveMarkerClient.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {String} [topic] - The topic to subscribe to, like '/basic_controls'
 *
 * @vue-data {ROS3D.InteractiveMarkerClient} object - Handle for the internal [ROS3D.InteractiveMarkerClient]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.InteractiveMarkerClient.html}
 */
export default {
  name: 'Ros3dInteractiveMarkerClient',
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
    }
  },
  watch: {
    topic(n) {
      this.object.unsubscribe()
      this.object.topicName = n
      this.object.subscribe()
    },
    visible(newState) {
      if (newState) this.show()
      else this.hide()
    }
  },
  mounted() {
    this.object = new ROS3D.InteractiveMarkerClient({
      ros: this.$parent.ros,
      tfClient: this.$parent.tfClient,
      rootObject: this.$parent.viewer.selectableObjects,
      camera: this.$parent.viewer.camera,
      topic: this.topic
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

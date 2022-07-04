<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

/**
 * A marker client that listens to a given marker topic.
 * It is a wrapper for [`ROS3D.MarkerClient`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.MarkerClient.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {String} [topic=] - The marker topic to listen to
 *
 * @vue-data {ROS3D.MarkerClient} object - Handle for the internal [ROS3D.MarkerClient]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.MarkerClient.html}
 */
export default {
  name: 'Ros3dMarkerClient',
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
    this.object = new ROS3D.MarkerClient({
      ros: this.$parent.ros,
      tfClient: this.$parent.tfClient,
      rootObject: this.$parent.viewer.scene,
      topic: this.topic
    })
    this.object.name = this._uid
    this.rosTopic = new ROSLIB.Topic({
      ros: this.$parent.ros,
      name: this.topic,
      messageType: 'visualization_msgs/Marker',
      compression: 'png'
    })
    this.rosTopic.subscribe(this.processMessage.bind(this))
    if (!this.visible) this.hide()
  },
  beforeDestroy() {
    this.object.unsubscribe(this.processMessage)
    this.rosTopic.unsubscribe()
    this.hide()
  },
  methods: {
    show() {
      this.$parent.viewer.scene.add(this.object)
    },
    hide() {
      var obj = this.$parent.viewer.scene.getObjectByName(this._uid)
      if (obj != null) this.$parent.viewer.scene.remove(obj)
    },
    removeMarker() {
      if (this.object) {
        for (var key in this.object.markers) {
          var oldNode = this.object.markers[key]
          if (!oldNode) {
            return
          }
          oldNode.unsubscribeTf()
          this.$parent.viewer.scene.remove(oldNode)
          oldNode.children.forEach(child => {
            child.dispose()
          })
          delete (this.object.markers[key])
        }
      }
    },
    processMessage(msg) {
      if (msg.action === 3) {
        this.removeMarker()
      }
    }
  }
}
</script>

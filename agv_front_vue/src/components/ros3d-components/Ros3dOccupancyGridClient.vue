<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */


/**
 * An occupancy grid client that listens to a given map topic.
 * It is a wrapper for [`ROS3D.OccupancyGridClient`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.OccupancyGridClient.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {String} [topic=] - The marker topic to listen to
 * @vue-prop {Number} [x=0] - X offset
 * @vue-prop {Number} [y=0] - Y offset
 * @vue-prop {Number} [z=0] - Z offset
 * @vue-prop {Boolean} [continuous=false] - If the map should be continuously loaded (e.g., for SLAM)
 *
 * @vue-data {ROS3D.OccupancyGridClient} object - Handle for the internal [ROS3D.OccupancyGridClient]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.OccupancyGridClient.html}
 */
export default {
  name: 'Ros3dOccupancyGridClient',
  props: {
    visible: {
      type: Boolean,
      default: true,
      require: false
    },
    color: {
      type: Object,
      default: function() {
        return { r: 255, g: 255, b: 255 }
      },
      require: false
    },
    topic: {
      type: String,
      default: '/map',
      require: false
    },
    x: {
      type: Number,
      default: 0,
      require: false
    },
    y: {
      type: Number,
      default: 0,
      require: false
    },
    z: {
      type: Number,
      default: 0,
      require: false
    },
    continuous: {
      type: Boolean,
      default: false,
      require: false
    }
  },
  watch: {
    topic(n) {
      this.object.unsubscribe()
      this.object.topicName = n
      this.object.subscribe()
    },
    continuous(n) {
      this.object.continuous = n
      if (n) this.object.subscribe()
    },
    x() {
      this.$nextTick(this.setOffset)
    },
    y() {
      this.$nextTick(this.setOffset)
    },
    z() {
      this.$nextTick(this.setOffset)
    },
    visible(newState) {
      if (newState) this.show()
      else this.hide()
    }
  },
  mounted() {
    this.object = new ROS3D.OccupancyGridClient({
      ros: this.$parent.ros,
      tfClient: this.$parent.tfClient,
      rootObject: this.$parent.viewer.scene,
      topic: this.topic,
      continuous: this.continuous,
      offsetPose: new ROSLIB.Pose({
        position: { x: this.x, y: this.y, z: this.z },
        color: this.color
      })
    })
    this.object.name = this._uid
    this.object.processMessage = (message) => {
      ROS3D.OccupancyGridClient.prototype.processMessage.call(
        this.object,
        message
      )
    }
    if (!this.visible) this.hide()
  },
  beforeDestroy() {
    this.hide()
  },
  methods: {
    show() {
      this.$parent.viewer.scene.add(this.object.sceneNode)
    },
    hide() {
      if (this.object.sceneNode != null) { this.$parent.viewer.scene.remove(this.object.sceneNode) }
    },
    setOffset() {
      this.object.unsubscribe()
      this.object.offsetPose = new ROSLIB.Pose({
        position: { x: this.x, y: this.y, z: this.z }
      })
      this.object.subscribe()
    }
  }
}
</script>

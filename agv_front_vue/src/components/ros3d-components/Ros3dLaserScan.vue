<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

/**
 * A LaserScan client that listens to a given topic and displays the points.
 * It is a wrapper for [`ROS3D.LaserScan`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.LaserScan.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {String} [topic=/scan] - The marker topic to listen to
 * @vue-prop {String} [compression=cbor] - Message compression
 * @vue-prop {Number} [max_pts=10000] - Number of points to draw
 * @vue-prop {Number} [pointRatio=1] - Point subsampling ratio (default: 1, no subsampling)
 * @vue-prop {Number} [messageRatio=1] - Message  subsampling ratio (default: 1, no subsampling)
 * @vue-prop {String} [color=#ff0000] - The color for the laser scan points
 *
 * @vue-data {ROS3D.LaserScan} object - Handle for the internal [ROS3D.LaserScan]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.LaserScan.html}
 */
export default {
  name: 'Ros3dLaserScan',
  props: {
    visible: {
      type: Boolean,
      default: true,
      require: false
    },
    topic: {
      type: String,
      default: '/scan',
      require: false
    },
    compression: {
      type: String,
      default: 'cbor',
      require: false
    },
    max_pts: {
      type: Number,
      default: 10000,
      require: false
    },
    pointRatio: {
      type: Number,
      default: 1,
      require: false
    },
    messageRatio: {
      type: Number,
      default: 1,
      require: false
    },
    color: {
      type: String,
      default: '#ff0000',
      require: false
    },
    particleSize: {
      type: Number,
      default: 0.25,
      require: false
    }
  },
  data: () => ({
    object: null
  }),
  watch: {
    visible(newState) {
      if (newState) this.show()
      else this.hide()
    },
    topic(n) {
      this.object.unsubscribe()
      this.object.topicName = n
      this.object.subscribe()
    },
    compression(n) {
      this.object.unsubscribe()
      this.object.compression = n
      this.object.subscribe()
    },
    max_pts() {
      this.$nextTick(this.createObject)
    },
    messageRatio() {
      this.$nextTick(this.createObject)
    },
    color() {
      this.$nextTick(this.createObject)
    },
    particleSize() {
      this.$nextTick(this.createObject)
    }
  },
  mounted() {
    this.createObject()
  },
  beforeDestroy() {
    this.object.unsubscribe()
    this.hide()
  },
  methods: {
    show() {
      this.object.subscribe()
      if (this.object.points.sn != null) this.$parent.viewer.scene.add(this.object.points.sn)
    },
    hide() {
      this.object.unsubscribe()
      if (this.object.points.sn != null) this.$parent.viewer.scene.remove(this.object.points.sn)
    },
    createObject() {
      if (this.object != null) this.hide()

      // Setup the laser scan.
      this.object = new ROS3D.LaserScan({
        ros: this.$parent.ros,
        tfClient: this.$parent.tfClient,
        rootObject: this.$parent.viewer.scene,
        topic: this.topic,
        compression: this.compression,
        max_pts: this.max_pts,
        pointRatio: this.pointRatio,
        messageRatio: this.messageRatio,
        material: {
          color: this.color,
          size: this.particleSize
        }
      })
      this.object.name = this._uid
      if (!this.visible) this.hide()
    }
  }
}
</script>

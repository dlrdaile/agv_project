<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

/**
 * A Path client that listens to a given topic and displays a line connecting the poses.
 * It is a wrapper for [`ROS3D.PointCloud2`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.PointCloud2.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {String} [topic=/points] - The PointCloud2 topic to listen to
 * @vue-prop {String} [compression=cbor] - Message compression
 * @vue-prop {Number} [max_pts=10000] - Number of points to draw
 * @vue-prop {Number} [pointRatio=1] - Point subsampling ratio (default: 1, no subsampling)
 * @vue-prop {Number} [messageRatio=1] - Message  subsampling ratio (default: 1, no subsampling)
 * @vue-prop {Number} [colorsrc=rgb] - The field to be used for coloring
 * @vue-prop {Object} [colormap] - Function that turns the colorsrc field value to a color
 * @vue-prop {Number} [particleSize=0.25] - Size of the particles
 * @vue-prop {String} [color=#009688] - The color to use for the particles
 *
 * @vue-data {ROS3D.PointCloud2} object - Handle for the internal [ROS3D.PointCloud2]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.PointCloud2.html}
 */
export default {
  name: 'Ros3dPointCloud2',
  props: {
    visible: {
      type: Boolean,
      default: true,
      require: false
    },
    topic: {
      type: String,
      default: '/points',
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
    colorsrc: {
      type: String,
      default: 'rgb',
      require: false
    },
    colormap: {
      type: Object,
      default: undefined,
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
    colorsrc() {
      this.$nextTick(this.createObject)
    },
    colormap() {
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

      // Setup the point cloud.
      this.object = new ROS3D.PointCloud2({
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

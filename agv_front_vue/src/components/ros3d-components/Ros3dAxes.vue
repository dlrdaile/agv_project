<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

/**
 * An Axes object can be used to display the axis of a particular coordinate frame.
 * It is a wrapper for [`ROS3D.Axes`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Axes.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {Number} [x=0] - Origin x
 * @vue-prop {Number} [y=0] - Origin y
 * @vue-prop {Number} [z=0] - Origin z
 * @vue-prop {Number} [scale=1] - The scale of the frame (defaults to 1.0)
 * @vue-prop {Number} [lineType=full] - The line type for the axes. Supported line types: 'dashed' and 'full'.
 * @vue-prop {Number} [lineDashLength=0.1] - The length of the dashes, relative to the length of the axis. Maximum value is 1, which means the dash length is equal to the length of the axis. Parameter only applies when lineType is set to dashed.
 * @vue-prop {Number} [headLength=0.1] - The head length to render
 * @vue-prop {Number} [shaftRadius=0.008] - The shaft radius to render
 * @vue-prop {Number} [headRadius=0.023] - The head radius to render
 *
 * @vue-data {ROS3D.Axes} object - Handle for the internal [ROS3D.Axes]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Axes.html}
 */
export default {
  name: 'Ros3dAxes',
  props: {
    visible: {
      type: Boolean,
      default: true,
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
    lineType: {
      type: String,
      default: 'full',
      require: false
    },
    lineDashLength: {
      type: Number,
      default: 0.1,
      require: false
    },
    scale: {
      type: Number,
      default: 1.0,
      require: false
    },
    headLength: {
      type: Number,
      default: 0.1,
      require: false
    },
    shaftRadius: {
      type: Number,
      default: 0.008,
      require: false
    },
    headRadius: {
      type: Number,
      default: 0.023,
      require: false
    }
  },
  watch: {
    visible(newState) {
      if (newState) this.show()
      else this.hide()
    },
    x() { this.$nextTick(this.setPosition) },
    y() { this.$nextTick(this.setPosition) },
    z() { this.$nextTick(this.setPosition) },
    lineType() { this.$nextTick(this.createObject) },
    lineDashLength() { this.$nextTick(this.createObject) },
    scale() { this.$nextTick(this.createObject) },
    headLength() { this.$nextTick(this.createObject) },
    shaftRadius() { this.$nextTick(this.createObject) },
    headRadius() { this.$nextTick(this.createObject) }
  },
  mounted() {
    this.createObject()
  },
  beforeDestroy() {
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
    createObject() {
      if (this.object != null) this.hide()

      this.object = new ROS3D.Axes({
        ros: this.$parent.ros,
        tfClient: this.$parent.tfClient,
        rootObject: this.$parent.viewer.scene,
        lineType: this.lineType,
        lineDashLength: this.lineDashLength,
        scale: this.scale,
        headLength: this.headLength,
        shaftRadius: this.shaftRadius,
        headRadius: this.headRadius
      })
      this.object.name = this._uid
      this.setPosition()
      if (this.visible) this.show()
    },
    setPosition() {
      this.object.position.set(this.x, this.y, this.z)
    }
  }
}
</script>

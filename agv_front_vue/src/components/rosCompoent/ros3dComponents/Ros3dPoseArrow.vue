<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

import * as Three from 'three'

/**
 * This is the same as the {@link Ros3dArrow}, but it directly takes a [`ROSLIB.Pose`]{@link http://robotwebtools.org/jsdoc/roslibjs/current/Pose.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {ROSLIB.Pose} [pose] - [ROSLIB.Pose]{@link http://robotwebtools.org/jsdoc/roslibjs/current/Pose.html} of the arrow
 * @vue-prop {Number} length (optional) - the length of the arrow
 * @vue-prop {Number} [headLength=1] - The head length of the arrow
 * @vue-prop {Number} [shaftDiameter=0.2] - The shaft diameter of the arrow
 * @vue-prop {Number} [headDiameter=0.05] - The head diameter of the arrow
 * @vue-prop {String} [color=#00ff00] - The color to use for this arrow
 *
 * @vue-data {ROS3D.Arrow} object - Handle for the internal [ROS3D.Arrow]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Arrow.html}
 */
export default {
  name: 'Ros3dPoseArrow',
  inheritAttrs: false,
  props: {
    visible: {
      type: Boolean,
      default: true,
      require: false
    },
    pose: {
      type: Object,
      default: undefined,
      require: false
    },
    length: {
      type: Number,
      default: 1,
      require: false
    },
    headLength: {
      type: Number,
      default: 0.2,
      require: false
    },
    shaftDiameter: {
      type: Number,
      default: 0.05,
      require: false
    },
    headDiameter: {
      type: Number,
      default: 0.1,
      require: false
    },
    color: {
      type: String,
      default: '#00ff00',
      require: false
    }
  },
  watch: {
    color(n) {
      this.object.material.color.set(n)
    },
    pose() { this.$nextTick(this.setPose) },
    length(n) {
      this.object.setLength(n)
    },
    visible(newState) {
      if (newState) this.show()
      else this.hide()
    }
  },
  mounted() {
    this.object = new ROS3D.Arrow({
      ros: this.$parent.ros,
      tfClient: this.$parent.tfClient,
      rootObject: this.$parent.viewer.scene,
      length: this.length,
      headLength: this.headLength,
      shaftDiameter: this.shaftDiameter,
      headDiameter: this.headDiameter,
      material: new Three.MeshBasicMaterial({ color: this.color })
    })
    this.object.name = this._uid

    this.setPose()

    if (this.visible) this.show()
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
    setPose() {
      if (this.pose === undefined) return

      this.object.position.set(this.pose.position.x, this.pose.position.y, this.pose.position.z)

      var rot = new Three.Quaternion(this.pose.orientation.x, this.pose.orientation.y,
        this.pose.orientation.z, this.pose.orientation.w)
      var direction = new Three.Vector3(1, 0, 0)
      direction.applyQuaternion(rot)

      this.object.setDirection(direction)
    }
  }
}
</script>

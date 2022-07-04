<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

import * as Three from 'three'

/**
 * An Arrow is a THREE object that can be used to display an arrow model.
 * It is a wrapper for [`ROS3D.Arrow`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Arrow.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {Number} [x=0] - Origin x
 * @vue-prop {Number} [y=0] - Origin y
 * @vue-prop {Number} [z=0] - Origin z
 * @vue-prop {Number} [directionX=1] - Direction x
 * @vue-prop {Number} [directionY=0] - Direction y
 * @vue-prop {Number} [directionZ=0] - Direction z
 * @vue-prop {Number} length (optional) - the length of the arrow
 * @vue-prop {Number} [headLength=1] - The head length of the arrow
 * @vue-prop {Number} [shaftDiameter=0.2] - The shaft diameter of the arrow
 * @vue-prop {Number} [headDiameter=0.05] - The head diameter of the arrow
 * @vue-prop {String} [color=#00ff00] - The color to use for this arrow
 *
 * @vue-data {ROS3D.Arrow} object - Handle for the internal [ROS3D.Arrow]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Arrow.html}
 */
export default {
  name: 'Ros3dArrow',
  inheritAttrs: false,
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
    directionX: {
      type: Number,
      default: 1,
      require: false
    },
    directionY: {
      type: Number,
      default: 0,
      require: false
    },
    directionZ: {
      type: Number,
      default: 0,
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
    x() { this.$nextTick(this.setPosition) },
    y() { this.$nextTick(this.setPosition) },
    z() { this.$nextTick(this.setPosition) },
    directionX() { this.$nextTick(this.setDirection) },
    directionY() { this.$nextTick(this.setDirection) },
    directionZ() { this.$nextTick(this.setDirection) },
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
      origin: new Three.Vector3(this.x || 0, this.y || 0, this.z || 0),
      direction: new Three.Vector3(this.directionX || 0, this.directionY || 0, this.directionZ || 0),
      length: this.length,
      headLength: this.headLength,
      shaftDiameter: this.shaftDiameter,
      headDiameter: this.headDiameter,
      material: new Three.MeshBasicMaterial({ color: this.color })
    })
    this.object.name = this._uid
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
    setPosition() {
      this.object.position.set(this.x, this.y, this.z)
    },
    setDirection() {
      this.object.setDirection(new Three.Vector3(this.directionX || 0, this.directionY || 0, this.directionZ || 0))
    }
  }
}
</script>

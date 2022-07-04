<template>
  <div>
    <slot v-if="loaded" />
  </div>
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

import TWEEN from '@tweenjs/tween.js'

// import * as ROS3D from "ros3d";
// import * as ROSLIB from "roslib";

import * as Three from 'three'
// var Three = window.Three = require('three');

// import { setTimeout, clearTimeout } from 'timers';

/**
 * @typedef {Object} TouchResult
 * @property {ROSLIB.Pose} pose - [`ROSLIB.Pose`]{@link http://robotwebtools.org/jsdoc/roslibjs/current/Pose.html} object relative to the `fixedFrame` TF frame
 * @property {number[]} screenPosition - X and Y coordinates on the screen
 */

/**
 * This is the root object all others are placed in.
 * It is more or less a wrapper for [`ROS3D.Viewer`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Viewer.html} with some additional logic for right-click/long-press handling and already integrates [`ROSLIB.TFClient`]{@link http://robotwebtools.org/jsdoc/roslibjs/current/TFClient.html}.
 *
 * @vue-prop {ROSLIB.Ros} ros - [ROSLIB.Ros]{@link http://robotwebtools.org/jsdoc/roslibjs/current/Ros.html} connection handle
 * @vue-prop {String} [background=#7e7e7e] - The color to render the background, like '#efefef'
 * @vue-prop {Boolean} [antialias=true] - If antialiasing should be used
 * @vue-prop {String} [fixedFrame=/map] - The fixed base frame for the tf listener
 * @vue-prop {Number} [longPressTolerance=15] - Tolerance in pixels for finger movement during long-press
 * @vue-prop {Number} [longPressDuration=750] - Duration for long-press in milliseconds
 *
 * @vue-data {ROS3D.Viewer} viewer - Handle for the internal [ROS3D.Viewer]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Viewer.html}
 * @vue-data {ROSLIB.TFClient} tfClient - Handle for the internal [ROSLIB.TFClient]{@link http://robotwebtools.org/jsdoc/roslibjs/current/TFClient.html}
 *
 * @vue-event {TouchResult} touch - Emitted on right-click or long-press. {@link TouchResult}
 */
export default {
  name: 'Ros3dViewer',
  props: {
    ros: {
      type: Object,
      require: true
    },
    background: {
      type: String,
      default: '#7e7e7e',
      require: false
    },
    antialias: {
      type: Boolean,
      default: true,
      require: false
    },
    fixedFrame: {
      type: String,
      default: '/map',
      require: false
    },
    longPressTolerance: {
      type: Number,
      default: 15,
      require: false
    },
    longPressDuration: {
      type: Number,
      default: 750,
      require: false
    }
  },
  data: () => ({
    viewer: null,
    tfClient: null,
    loaded: false,
    hold: false,
    position: null,
    direction: null,
    screenPosition: null
  }),
  watch: {
    hold(n, o) {
      if (n && !o) {
        this.viewer.scene.add(this.arrow)
      } else if (o && !n) {
        this.viewer.scene.remove(this.arrow)
      }
    },
    position(n) {
      if (n != null) {
        this.arrow.position.set(n.x, n.y, n.z + 0.05)
        this.circle.position.set(n.x, n.y, n.z + 0.05)
      }
    },
    direction(n) {
      if (n != null) this.arrow.setDirection(n)
    }
  },
  mounted() {
    this.$el.id = 'viewer'
    // Create the main viewer.
    // eslint-disable-next-line no-undef
    this.viewer = new ROS3D.Viewer({
      divID: this.$el.id,
      width: this.$el.clientWidth,
      height: this.$el.clientHeight,
      antialias: this.antialias,
      background: this.background,
      displayPanAndZoomFrame: true,
      cameraPose: {
        x: 8,
        y: 7,
        z: 5
      }
    })

    // Add TWEEN.update() to draw loop (for smooth animations)
    this.viewer.draw = () => {
      TWEEN.update()
      // eslint-disable-next-line no-undef
      ROS3D.Viewer.prototype.draw.call(this.viewer)
    }

    // Setup a client to listen to TFs.
    this.tfClient = new ROSLIB.TFClient({
      ros: this.ros,
      angularThres: 0.01,
      transThres: 0.01,
      rate: 10.0,
      fixedFrame: this.fixedFrame
    })
    // listen to DOM events
    var eventNames = [
      'contextmenu',
      'click',
      'mouseout',
      'mousedown',
      'mouseup',
      'mousemove',
      'touchstart',
      'touchend',
      'touchcancel',
      'touchleave',
      'touchmove'
    ]
    this.listeners = {}

    // add event listeners for the associated mouse events
    eventNames.forEach((eventName) => {
      this.listeners[eventName] = this.processDomEvent.bind(this)
      this.$el.addEventListener(eventName, this.listeners[eventName], true)
    }, this)

    // For debug reason
    window.scene = window.Scene = this.viewer.scene

    // Create arrow for touch-and-hold or right-click
    // eslint-disable-next-line no-undef
    this.arrow = new ROS3D.Arrow({
      ros: this.ros,
      tfClient: this.tfClient,
      rootObject: this.viewer.scene,
      material: new Three.MeshBasicMaterial({ color: 0xff0000 })
    })

    // Create circle for touchdown animation
    var geometry = new Three.CircleGeometry(1, 32)
    var material = new Three.MeshPhongMaterial({
      color: 0x000000,
      specular: 0x666666,
      emissive: 0x994400,
      shininess: 0,
      opacity: 0.5,
      transparent: true
    })
    this.circle = new Three.Mesh(geometry, material)
    this.circle.visible = false
    this.circle.scale.set(0, 0, 0)
    this.viewer.scene.add(this.circle)

    this.loaded = true
  },
  methods: {
    startTimer() {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => (this.hold = true), this.longPressDuration)
    },
    stopTimer() {
      if (this.timer) {
        clearTimeout(this.timer)
        this.timer = undefined
      }
      this.hold = false
      this.position = null
      this.direction = null
      this.screenPosition = null

      this.circle.visible = false
      this.circle.scale.set(0, 0, 0)
    },
    processDomEvent(domEvent) {
      this.$emit(domEvent.type)

      // if the mouse/touch leaves the dom element, stop everything
      if (
        domEvent.type === 'mouseout' ||
        domEvent.type === 'touchleave' ||
        domEvent.type === 'touchcancel'
      ) {
        this.stopTimer()
        return
      }

      if (
        domEvent.type === 'mouseup' ||
        domEvent.type === 'click' ||
        domEvent.type === 'touchend'
      ) {
        if (this.hold) {
          var quat = new Three.Quaternion()
          this.arrow.getWorldQuaternion(quat)

          quat = quat.multiply(
            new Three.Quaternion(0, 0, Math.sqrt(0.5), Math.sqrt(0.5))
          )

          this.$emit('touch', {
            pose: new ROSLIB.Pose({
              position: new ROSLIB.Vector3({
                x: this.position.x,
                y: this.position.y
              }),
              orientation: new ROSLIB.Quaternion({
                x: quat.x,
                y: quat.y,
                z: quat.z,
                w: quat.w
              })
            }),
            screenPosition: this.screenPosition
          })
        }
        this.stopTimer()
        return
      }

      var pos_x, pos_y

      if (domEvent.type.indexOf('touch') !== -1) {
        pos_x = 0
        pos_y = 0
        for (var i = 0; i < domEvent.touches.length; ++i) {
          pos_x += domEvent.touches[i].clientX
          pos_y += domEvent.touches[i].clientY
        }
        pos_x /= domEvent.touches.length
        pos_y /= domEvent.touches.length
      } else {
        pos_x = domEvent.clientX
        pos_y = domEvent.clientY
      }

      // Calculate the touch position in ROS space
      var vec = new Three.Vector3() // create once and reuse
      var pos = new Three.Vector3() // create once and reuse
      vec.set(
        (pos_x / window.innerWidth) * 2 - 1,
        -(pos_y / window.innerHeight) * 2 + 1,
        0.5
      )

      vec.unproject(this.viewer.camera)
      vec.sub(this.viewer.camera.position).normalize()
      var distance = -this.viewer.camera.position.z / vec.z
      pos.copy(this.viewer.camera.position).add(vec.multiplyScalar(distance))

      var scaleVector, scaleFactor, scale

      if (domEvent.type === 'mousedown' && domEvent.button === 2) {
        // Right click
        this.hold = true
        this.position = pos
        this.screenPosition = [pos_x, pos_y]

        // Make touch group scale independent of camera
        scaleVector = new Three.Vector3()
        scaleFactor = 20
        scale =
          scaleVector
            .subVectors(this.position, this.viewer.camera.position)
            .length() / scaleFactor
        this.arrow.scale.set(scale, scale, 1)

        return
      } else if (
        domEvent.type === 'touchmove' ||
        domEvent.type === 'mousemove'
      ) {
        if (this.hold) {
          this.hold = true
          this.direction = pos.sub(this.position)
          domEvent.stopPropagation()
        } else if (
          this.screenPosition == null ||
          Math.sqrt(
            (this.screenPosition[0] - pos_x) *
              (this.screenPosition[0] - pos_x) +
              (this.screenPosition[1] - pos_y) *
                (this.screenPosition[1] - pos_y)
          ) > this.longPressTolerance
        ) {
          this.stopTimer()
        }
        return
      } else if (domEvent.type === 'touchstart') {
        this.position = pos
        this.screenPosition = [pos_x, pos_y]
        this.startTimer()

        // Make touch group scale independent of camera
        scaleVector = new Three.Vector3()
        scaleFactor = 10
        scale =
          scaleVector
            .subVectors(this.position, this.viewer.camera.position)
            .length() / scaleFactor
        this.arrow.scale.set(scale, scale, 1)

        this.circle.visible = true
        if (this.circleScaleTween) this.circleScaleTween.stop()
        this.circle.scale.set(0, 0, 0)
        this.circleScaleTween = new TWEEN.Tween(this.circle.scale.clone())
          .to(new Three.Vector3(scale, scale, 1), this.longPressDuration)
          .easing(TWEEN.Easing.Back.InOut)
          .onUpdate((obj) => {
            this.circle.scale.copy(obj)
          })
          .start()
      }
    }
  }
}
</script>

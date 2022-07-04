<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

/**
 * A SceneNode can be used to keep track of a 3D object with respect to a ROS frame within a scene.
 * It is more or less a wrapper for [`ROS3D.SceneNode`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.SceneNode.html}.
 *
 * @vue-prop {Object} model - The THREE 3D object to be rendered
 * @vue-prop {String} [frameID=base_link] - The frame ID this object belongs to
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 *
 * @vue-data {ROS3D.SceneNode} object - Handle for the internal [ROS3D.SceneNode]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.SceneNode.html}
 */
export default {
  name: 'Ros3dSceneNode',
  props: {
    model: {
      type: Object,
      require: true,
      default: null
    },
    frameID: {
      type: String,
      default: 'base_link',
      require: false
    },
    visible: {
      type: Boolean,
      default: true,
      require: false
    }
  },
  watch: {
    model() {
      this.$nextTick(this.createObject)
    },
    frameID() {
      this.$nextTick(this.createObject)
    },
    visible(newState) {
      if (newState) this.show()
      else this.hide()
    }
  },
  beforeDestroy() {
    this.object.unsubscribeTf()
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

      if (this.model != null) {
        this.object = new ROS3D.SceneNode({
          tfClient: this.$parent.tfClient,
          frameID: this.frameID,
          object: this.model
        })
        this.object.name = this._uid

        // This is not done automatically
        this.show()
      }
    }
  }
}
</script>

<template>
  <div />
</template>

<script>
/**
 * @author Ludwig Waffenschmidt - ludwig.waffenschmidt@outlook.com
 */

/**
 * Create a grid object.
 * It is a wrapper for [`ROS3D.Grid`]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Grid.html}.
 *
 * @vue-prop {Boolean} [visible=true] - Visibility of this object
 * @vue-prop {Number} [numCells=10] - The number of cells of the grid
 * @vue-prop {Number} [lineWidth=1] - The width of the lines in the grid
 * @vue-prop {Number} [cellSize=1] - The length, in meters, of the side of each cell
 * @vue-prop {String} [color=#cccccc] - The line color of the grid
 *
 * @vue-data {ROS3D.Grid} object - Handle for the internal [ROS3D.Grid]{@link http://robotwebtools.org/jsdoc/ros3djs/current/ROS3D.Grid.html}
 */
export default {
  name: 'Ros3dGrid',
  props: {
    visible: {
      type: Boolean,
      default: true,
      require: false
    },
    numCells: {
      type: Number,
      default: 10,
      require: false
    },
    color: {
      type: String,
      default: '#cccccc',
      require: false
    },
    lineWidth: {
      type: Number,
      default: 1,
      require: false
    },
    cellSize: {
      type: Number,
      default: 1,
      require: false
    }
  },
  watch: {
    visible(newState) {
      if (newState) this.show()
      else this.hide()
    },
    numCells() {
      this.$nextTick(this.createObject)
    },
    color() {
      this.$nextTick(this.createObject)
    },
    lineWidth() {
      this.$nextTick(this.createObject)
    },
    cellSize() {
      this.$nextTick(this.createObject)
    }
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

      this.object = new ROS3D.Grid({
        num_cells: this.numCells,
        color: this.color,
        lineWidth: this.lineWidth,
        cellSize: this.cellSize
      })
      this.object.name = this._uid

      if (this.visible) this.show()
    }
  }
}
</script>

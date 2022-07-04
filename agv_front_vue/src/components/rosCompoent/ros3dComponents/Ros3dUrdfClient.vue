<template>
  <div class="urdf-container" />
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      default: true,
      require: false
    },
    param: {
      type: String,
      require: false,
      default: 'robot_description'
    },
    path: {
      type: String,
      require: false,
      default: document.location.origin
    },
    tfPrefix: {
      require: false,
      type: String,
      default: ''
    },
    loader: {
      require: false,
      type: Object,
      default: ROS3D.COLLADA_LOADER_2
    }
  },
  data() {
    return {
      object: null
    }
  },
  mounted() {
    this.createObject()
  },
  beforeDestroy() {
    this.hide()
  },
  // watch: {
  //   visible(){
  //     if(this.visible)
  //     {
  //       this.show()
  //     }
  //     else{
  //       this.hide()
  //     }
  //   }
  // },
  methods: {
    show() {
      this.$parent.viewer.scene.add(this.object.urdf)
      console.log('show')
    },
    hide() {
      if (this.object.urdf != null) { console.log('hide') }
      this.$parent.viewer.scene.remove(this.object.urdf)
    },
    createObject() {
      if (this.object != null) this.hide()
      this.object = new ROS3D.UrdfClient({
        ros: this.$parent.ros,
        tfClient: this.$parent.tfClient,
        rootObject: this.$parent.viewer.scene,
        path: this.path,
        loader: this.loader,
        tfPrefix: this.tfPrefix,
        param: this.param
      })
      this.object.name = this._uid
      if (!this.visible) this.hide()
    }
  }
}
</script>

<style>
</style>

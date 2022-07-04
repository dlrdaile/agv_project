<template>
  <div id="app" class="app-container">
    <battery />
    <ros-panel />
    <vue-nipple
      v-if="refresh"
      :color="color"
      :max-number-of-nipples="maxNumberOfNipples"
      :multitouch="multitouch"
      :mode="mode"
      class-name="nipple1"
      :dynamic-page="dynamicPage"
      :follow="follow"
      :size="size"
      style="background-color: lightgreen; height: 200px"
      :lock-x="true"
      @move="added"
    />
  </div>
</template>

<script>
import Battery from '@/components/rosCompoent/rosStatus/Battery.vue'
import VueNipple from '@/components/rosCompoent/RosCtrl/Nipple.vue'
import RosPanel from '@/views/rosPanel/component/MainBodyComponent/RosSceneArea'
export default {
  components: {
    Battery,
    VueNipple,
    RosPanel
  },
  data() {
    return {
      color: 'red',
      maxNumberOfNipples: 2,
      mode: 'semi',
      follow: true,
      dynamicPage: true,
      multitouch: true,
      refresh: true,
      position: { bottom: '20%', left: '15%' },
      size: 150
    }
  },
  methods: {
    added(val) {
      console.log(val.vector.x + ',' + val.vector.y)
      // console.log(val.instance.frontPosition.x+','+val.instance.frontPosition.y);
    }
  }
}
</script>

<style lang="less">
* {
  margin: 0;
  padding: 0;
}

.app-container {
  width: 100%;
  height: 100%;
}
</style>

<template>
  <div class="rosmain-container">
    <div class="ros-scene-area">
      <ros-scene-area
        :rosview-object="rosviewObject"
      />
    </div>
  </div>
</template>

<script>
import rosSceneArea from '@/views/rosPanel/component/MainBodyComponent/RosSceneArea'
import RosKeyCmd from '@/components/rosCompoent/RosCtrl/RosKeyCmd'
import Nipple from '@/components/rosCompoent/RosCtrl/Nipple'
export default {
  name: 'MainBody',
  components: {
    rosSceneArea,
    RosKeyCmd,
    Nipple
  },
  data() {
    return {
      rosviewObject: {
        width: '500px',
        height: '500px'
      }
    }
  }
}
</script>

<style scoped>
.rosmain-container{
  width: 100%;
  height: 100%;
  background-color: pink;
}
</style>

<template>
  <div class="ros3d-container">
    <ros3d-viewer
      v-if="connected"
      :ros="ros"
      class="ros_view"
      :background="backgroud_color"
      :fixed-frame="'map'"
      :style="rosviewObject"
    >
      <ros3d-occupancy-grid-client />
      <ros3d-axes />
      <ros3d-grid />
      <ros3d-odom
        :keep="5"
      />
      <ros3d-urdf-client />
      <ros3d-laser-scan />
      <ros3d-path topic="/move_base/GlobalPlanner/plan" />
      <ros3d-path topic="/move_base/DWAPlannerROS/local_plan" color="#000000" />
      <ros3d-marker-client topic="/visualization_marker" />
      <ros3d-pose-array topic="/particlecloud" />
      <!-- <ros3d-marker-client topic="/visualization_marker"></ros3d-marker-client> -->
    </ros3d-viewer>
  </div>
</template>

<script>
import {
  Ros3dViewer,
  Ros3dGrid,
  Ros3dAxes,
  Ros3dPath,
  Ros3dOccupancyGridClient,
  Ros3dOdom,
  Ros3dLaserScan,
  Ros3dUrdfClient,
  Ros3dMarkerClient,
  Ros3dPoseArray
} from '@/components/rosCompoent/ros3dComponents'

export default {
  components: {
    Ros3dViewer,
    Ros3dPath,
    Ros3dGrid,
    Ros3dAxes,
    Ros3dUrdfClient,
    Ros3dOccupancyGridClient,
    Ros3dOdom,
    Ros3dLaserScan,
    Ros3dMarkerClient,
    Ros3dPoseArray
  },
  props: {
    rosviewObject: {
      type: Object,
      default: function() {
        return {
          width: '500px',
          height: '500px'
        }
      }
    },
    ros: {
      type: Object,
      default: null,
      require: true
    },
    connected: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    backgroud_color: '#070e1f',
    isshow: true
  })
}
</script>

<style lang="scss" scoped>
.ros3d-container {
  .ros_view {
    position: absolute;
    border: 1px solid;
  }
}
</style>

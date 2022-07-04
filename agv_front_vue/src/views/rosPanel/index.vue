<template>
  <div class="rospanel-container">
    <el-container>
      <el-header style="padding-left: 0">
        <ros-heade />
      </el-header>
      <el-main>
        <ros-main />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import RosHeade from '@/views/rosPanel/component/Header'
import RosMain from '@/views/rosPanel/component/MainBody'

export default {
  name: 'RosPanel',
  components: {
    RosHeade,
    RosMain
  }
}
</script>

<style scoped lang="scss">
.el-container {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: url("../../assets/images/bg.png"); //背景图
}
</style>

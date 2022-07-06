<!--
针对于 /hotpage 这条路径而显示出来的
在这个组件中, 通过子组件注册的方式, 要显示出Hot.vue这个组件
-->
<template>
  <div class="com-page">
    <hot />
  </div>
</template>

<script>
import Hot from '@/components/OrderPanelComponent/Hot'
export default {
  components: {
    hot: Hot
  },
  data() {
    return {}
  },
  methods: {}
}
</script>

<style lang="less" scoped>
</style>

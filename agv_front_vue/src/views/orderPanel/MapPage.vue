<!--
针对于 /mappage 这条路径而显示出来的
在这个组件中, 通过子组件注册的方式, 要显示出Map.vue这个组件
-->
<template>
  <div class="com-page">
    <single-map />
  </div>
</template>

<script>
import Map from '@/components/OrderPanelComponent/Map'
export default {
  components: {
    'single-map': Map
  },
  data() {
    return {}
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
</style>

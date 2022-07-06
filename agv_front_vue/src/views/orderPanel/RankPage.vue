<!--
针对于 /rankpage 这条路径而显示出来的
在这个组件中, 通过子组件注册的方式, 要显示出Rank.vue这个组件
-->
<template>
  <div class="com-page">
    <rank />
  </div>
</template>

<script>
import Rank from '@/components/OrderPanelComponent/Rank'
export default {
  components: {
    rank: Rank
  },
  data() {
    return {}
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
</style>

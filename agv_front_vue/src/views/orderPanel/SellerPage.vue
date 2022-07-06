<!--
针对于 /sellerpage 这条路径而显示出来的
在这个组件中, 通过子组件注册的方式, 要显示出Seller.vue这个组件
 -->
<template>
  <div class="com-page">
    <seller />
  </div>
</template>

<script>
import Seller from '@/components/OrderPanelComponent/Seller'
export default {
  components: {
    seller: Seller
  },
  data() {
    return {}
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
</style>

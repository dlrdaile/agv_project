<template>
  <div class="screen-container" :style="containerStyle">
    <header class="screen-header">
      <div>
        <img :src="headerSrc" alt="">
      </div>
      <!-- <span class="logo">
        <img :src="logoSrc" alt="" />
      </span> -->
      <span class="title">订单大数据监控系统</span>
      <div class="title-right">
        <img :src="themeSrc" class="qiehuan" @click="handleChangeTheme">
        <span class="datetime">2022-07-04 </span>
      </div>
    </header>
    <div class="screen-body">
      <section class="screen-left">
        <div id="left-top" :class="[fullScreenStatus.trend ? 'fullscreen' : '']">
          <!-- 销量趋势图表 -->
          <Trend ref="trend" />
          <div class="resize">
            <!-- icon-compress-alt 可以转换大小-->
            <span :class="['iconfont', fullScreenStatus.trend ? 'icon-compress-alt' : 'icon-expand-alt']" @click="changeSize('trend')" />
          </div>
        </div>
        <div id="left-bottom" :class="[fullScreenStatus.seller ? 'fullscreen' : '']">
          <!-- 商家销售金额图表 -->
          <Seller ref="seller" />
          <div class="resize">
            <!-- icon-compress-alt -->
            <span :class="['iconfont', fullScreenStatus.seller ? 'icon-compress-alt' : 'icon-expand-alt']" @click="changeSize('seller')" />
          </div>
        </div>
      </section>
      <section class="screen-middle">
        <div id="middle-top" :class="[fullScreenStatus.map ? 'fullscreen' : '']">
          <!-- 商家分布图表 -->
          <Map ref="map" />
          <div class="resize">
            <!-- icon-compress-alt -->
            <span :class="['iconfont', fullScreenStatus.map ? 'icon-compress-alt' : 'icon-expand-alt']" @click="changeSize('map')" />
          </div>
        </div>
        <div id="middle-bottom" :class="[fullScreenStatus.rank ? 'fullscreen' : '']">
          <!-- 地区销量排行图表 -->
          <Rank ref="rank" />
          <div class="resize">
            <!-- icon-compress-alt -->
            <span :class="['iconfont', fullScreenStatus.rank ? 'icon-compress-alt' : 'icon-expand-alt']" @click="changeSize('rank')" />
          </div>
        </div>
      </section>
      <section class="screen-right">
        <div id="right-top" :class="[fullScreenStatus.hot ? 'fullscreen' : '']">
          <!-- 热销商品占比图表 -->
          <Hot ref="hot" />
          <div class="resize">
            <!-- icon-compress-alt -->
            <span :class="['iconfont', fullScreenStatus.hot ? 'icon-compress-alt' : 'icon-expand-alt']" @click="changeSize('hot')" />
          </div>
        </div>
        <div id="right-bottom" :class="[fullScreenStatus.stock ? 'fullscreen' : '']">
          <!-- 库存销量分析图表 -->
          <Stock ref="stock" />
          <div class="resize">
            <!-- icon-compress-alt -->
            <span :class="['iconfont', fullScreenStatus.stock ? 'icon-compress-alt' : 'icon-expand-alt']" @click="changeSize('stock')" />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import Hot from '@/components/OrderPanelComponent/Hot.vue'
import Map from '@/components/OrderPanelComponent/Map.vue'
import Rank from '@/components/OrderPanelComponent/Rank.vue'
import Seller from '@/components/OrderPanelComponent/Seller.vue'
import Stock from '@/components/OrderPanelComponent/Stock.vue'
import Trend from '@/components/OrderPanelComponent/Trend.vue'
import { getThemeValue } from '@/utils/theme_utils'
export default {
  components: {
    Hot,
    Map,
    Rank,
    Seller,
    Stock,
    Trend
  },
  data() {
    return {
      // 定义每一个图表的全屏状态
      fullScreenStatus: {
        trend: false,
        seller: false,
        map: false,
        rank: false,
        hot: false,
        stock: false
      },
      socket: null
    }
  },
  computed: {
    logoSrc() {
      return '/static/img/' + getThemeValue(this.theme).logoSrc
    },
    headerSrc() {
      return '/static/img/' + getThemeValue(this.theme).headerBorderSrc
    },
    themeSrc() {
      return '/static/img/' + getThemeValue(this.theme).themeSrc
    },
    containerStyle() {
      return {
        backgroundColor: getThemeValue(this.theme).backgroundColor,
        color: getThemeValue(this.theme).titleColor
      }
    },
    theme() {
      return this.$store.getters.orderPanelTheme
    }
  },
  created() {
    // 注册接收到数据的回调函数
    // 对服务端进行websocket的连接
    this.$socket.connect()
    this.$socket.registerCallBack('fullScreen', this.recvData)
    this.$socket.registerCallBack('themeChange', this.recvThemeChange)
  },
  destroyed() {
    this.$socket.unRegisterCallBack('fullScreen')
    this.$socket.unRegisterCallBack('themeChange')
    this.$socket.close()
  },
  methods: {
    changeSize(chartName) {
      // 1.改变fullScreenStatus的数据
      // this.fullScreenStatus[chartName] = !this.fullScreenStatus[chartName]
      // 2.需要调用每一个图表组件的screenAdapter的方法
      // this.$refs[chartName].screenAdapter()
      // this.$nextTick(() => {
      //   this.$refs[chartName].screenAdapter()
      // })
      // 将数据发送给服务端
      const targetValue = !this.fullScreenStatus[chartName]
      this.$socket.send({
        action: 'fullScreen',
        socketType: 'fullScreen',
        chartName: chartName,
        value: targetValue
      })
    },
    // 接收到全屏数据之后的处理
    recvData(data) {
      // 取出是哪一个图表需要进行切换
      const chartName = data.chartName
      // 取出, 切换成什么状态
      const targetValue = data.value
      console.log(data)
      this.fullScreenStatus[chartName] = targetValue
      this.$nextTick(() => {
        this.$refs[chartName].screenAdapter()
      })
    },
    handleChangeTheme() {
      // 修改VueX中数据
      // this.$store.commit('changeTheme')
      this.$socket.send({
        action: 'themeChange',
        socketType: 'themeChange',
        chartName: '',
        value: ''
      })
    },
    recvThemeChange() {
      this.$store.commit('theme/changeTheme')
    }
  }
}
</script>
<style lang="scss" scoped>
.fullscreen {
  position: fixed!important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  margin: 0 !important;
  z-index: 100;
}

.screen-container {
  position: absolute;
  width: 100%;
  height: 100%;
  padding: 0 20px;
  background-color: #161522;
  color: #fff;
  box-sizing: border-box;
}
.screen-header {
  width: 100%;
  height: 64px;
  font-size: 20px;
  position: relative;
  > div {
      img {
        width: 100%;
      }
    }
  .title {
    position: absolute;
    left: 50%;
    top: 50%;
    font-size: 20px;
    transform: translate(-50%, -50%);
  }
  .title-right {
    display: flex;
    align-items: center;
    position:absolute;
    right: 0px;
    top: 50%;
    transform: translateY(-80%);
  }
  .qiehuan {
    width: 28px;
    height: 21px;
    cursor: pointer;
  }
  .datetime {
    font-size: 15px;
    margin-left: 10px;
  }
  .logo {
    position: absolute;
    left: 0px;
    top: 50%;
    transform: translateY(-80%);
    img {
      height: 35px;
      width: 128px;
    }
  }
}
.screen-body {
  width: 100%;
  height: 100%;
  display: flex;
  margin-top: 10px;
  .screen-left {
    height: 100%;
    width: 27.6%;
    #left-top {
      height: 53%;
      position: relative;
    }
    #left-bottom {
      height: 31%;
      margin-top: 25px;
      position: relative;
    }
  }
  .screen-middle {
    height: 100%;
    width: 41.5%;
    margin-left: 1.6%;
    margin-right: 1.6%;
    #middle-top {
      width: 100%;
      height: 56%;
      position: relative;
    }
    #middle-bottom {
      margin-top: 25px;
      width: 100%;
      height: 28%;
      position: relative;
    }
  }
  .screen-right {
    height: 100%;
    width: 27.6%;
    #right-top {
      height: 46%;
      position: relative;
    }
    #right-bottom {
      height: 38%;
      margin-top: 25px;
      position: relative;
    }
  }
}
.resize {
  position: absolute;
  right: 20px;
  top: 20px;
  cursor: pointer;
}
</style>

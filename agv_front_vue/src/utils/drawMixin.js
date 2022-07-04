// 屏幕适配 mixin 函数

// * 默认缩放值
const scale = {
  width: '1',
  height: '1'
}

// * 设计稿尺寸（px）
const baseWidth = 1920
const baseHeight = 1080

// * 需保持的比例（默认1.77778）
const baseProportion = parseFloat((baseWidth / baseHeight).toFixed(5))

export default {
  data() {
    return {
      // * 定时函数
      drawTiming: null
    }
  },
  mounted() {
    // 进入触发
    this.calcRate()
    window.addEventListener('resize', this.resize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resize)
  },
  methods: {
    calcRate() {
      // 拿到整个页面元素
      const appRef = this.$refs['appRef']
      // 如果没有值就结束
      if (!appRef) return
      // 当前宽高比
      const currentRate = parseFloat((window.innerWidth / window.innerHeight).toFixed(5))
      // 判断：如果有值代表页面变化了
      if (appRef) {
        // 判断当前宽高比例是否大于默认比例
        if (currentRate > baseProportion) {
          // 如果大于代表更宽了，就是放大了
          // 那么把默认缩放的宽高改为：同比例放大
          scale.width = ((window.innerHeight * baseProportion) / baseWidth).toFixed(5)
          scale.height = (window.innerHeight / baseHeight).toFixed(5)
          console.log(scale.width, scale.height, '放大')
          // 整个页面的元素样式，缩放宽高用当前同比例放大的宽高
          appRef.style.transform = `scale(${scale.width}, ${scale.height}) translate(-50%, -50%)`
        } else {
          // 如果不大于默认比例代表缩小了。
          // 那么把默认缩放的宽高改为：同比例缩小
          scale.height = ((window.innerWidth / baseProportion) / baseHeight).toFixed(5)
          scale.width = (window.innerWidth / baseWidth).toFixed(5)
          console.log(scale.width, scale.height, '缩小')
          // 整个页面的元素样式，缩放宽高用当前同比例放大的宽高
          appRef.style.transform = `scale(${scale.width}, ${scale.height}) translate(-50%, -50%)`
        }
      }
    },
    resize() {
      clearTimeout(this.drawTiming)
      this.drawTiming = setTimeout(() => {
        this.calcRate()
      }, 200)
    }
  }
}

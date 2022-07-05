<template>
  <div class="speed-chart" ref="chartFieldRef"/>
</template>
<script>
export default {
  name: 'SpeedChart',
  props: {
    title: {
      type: String,
      default: '12'
    },
    formatFunction: {
      type: Function,
      default: function(value) {
        return value
      }
    },
    dataArr: {
      type: Number,
      default: 0
    },
    vmax: {
      type: Number,
      default: 10
    },
    colorSet: {
      type: Object,
      default: function() {
        return {
          color: '#468EFD'
        }
      }
    }
  },
  data() {
    return {
      chart: null
    }
  },
  computed: {
    option() {
      return {
        backgroundColor: '#0E1327',
        tooltip: {
          formatter: '{a} <br/>{b} : {c}%'
        },
        series: [
          {
            name: '内部进度条',
            type: 'gauge',
            // center: ['20%', '50%'],
            radius: '72%',
            max: this.vmax,
            splitNumber: 10,
            axisLine: {
              lineStyle: {
                color: [
                  [this.dataArr / this.vmax, this.colorSet.color],
                  [1, '#111F42']
                ],
                width: 4
              }
            },
            axisLabel: {
              show: false
            },
            axisTick: {
              show: false
            },
            splitLine: {
              show: false
            },
            itemStyle: {
              show: false
            },
            detail: {
              formatter: this.formatFunction,
              offsetCenter: [0, 50],
              textStyle: {
                padding: [0, 0, 0, 0],
                fontSize: 15,
                fontWeight: '500',
                color: this.colorSet.color
              }
            },
            title: {
              // 标题
              show: true,
              offsetCenter: [0, 70], // x, y，单位px
              textStyle: {
                color: '#fff',
                fontSize: 14, // 表盘上的标题文字大小
                fontWeight: 400,
                fontFamily: 'PingFangSC'
              }
            },
            data: [
              {
                name: this.title,
                value: this.dataArr
              }
            ],
            pointer: {
              show: true,
              length: '80%',
              radius: '20%',
              width: 4 // 指针粗细
            },
            animationDuration: 4000
          },
          {
            name: '外部刻度',
            type: 'gauge',
            //  center: ['20%', '50%'],
            radius: '65%',
            min: 0, // 最小刻度
            max: this.vmax, // 最大刻度
            splitNumber: 5, // 刻度数量
            startAngle: 225,
            endAngle: -45,
            axisLine: {
              show: true,
              lineStyle: {
                width: 1,
                color: [[1, 'rgba(0,0,0,0)']]
              }
            }, // 仪表盘轴线
            axisLabel: {
              show: true,
              color: '#4d5bd1',
              distance: 25
            }, // 刻度标签。
            axisTick: {
              show: true,
              splitNumber: 7,
              lineStyle: {
                color: this.colorSet.color, // 用颜色渐变函数不起作用
                width: 1
              },
              length: -6
            }, // 刻度样式
            splitLine: {
              show: true,
              length: -15,
              lineStyle: {
                color: this.colorSet.color // 用颜色渐变函数不起作用
              }
            }, // 分隔线样式
            detail: {
              show: false
            },
            pointer: {
              show: false
            }
          }
        ]
      }
    }
  },
  watch: {
    option: {
      handler: function(n, o) {
        this.chart.setOption(n)
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    // const chartField = document.getElementById('chartField')
    this.chart = this.$echarts.init(this.$refs.chartFieldRef)
    window.onresize = this.chart.resize
    this.chart.setOption(this.option)
  }
}
</script>

<style scoped>

</style>

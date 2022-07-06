<template>
  <div ref="chartFieldRef" class="press-chart" />
</template>
<script>
export default {
  name: 'PressChart',
  props: {
    value: {
      type: Number,
      default: 0
    },
    vmax: {
      type: Number,
      default: 5
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
        series: [
          {
            center: ['50%', '50%'], // 仪表的位置
            name: '压力表', // 仪表的名字
            type: 'gauge', // 统计图类型为仪表
            radius: '82%', // 统计图的半径大小
            min: 0, // 最小刻度
            max: this.vmax, // 最大刻度
            splitNumber: 5, // 刻度数量
            startAngle: 225, // 开始刻度的角度
            endAngle: -45, // 结束刻度的角度
            axisLine: {
              // 设置默认刻度盘上的刻度不显示，重新定义刻度盘
              show: false,
              lineStyle: {
                width: 1,
                color: [[1, 'rgba(255,255,255,0)']]
              }
            }, // 仪表盘轴线
            axisLabel: {
              // 仪表盘上的数据
              show: true,
              color: '#4d5bd1', // 仪表盘上的轴线颜色
              distance: 25, // 图形与刻度的间距
              formatter: function(v) {
                // 刻度轴上的数据相关显示
                return parseFloat(v).toFixed(1)
              }
            }, // 刻度标签。
            axisTick: {
              show: true,
              splitNumber: 5, // 刻度的段落数
              lineStyle: {
                color: '#fff',
                width: 1 // 刻度的宽度
              },
              length: -6 // 刻度的长度
            }, // 刻度样式
            splitLine: {
              // 文字和刻度的偏移量
              show: true,
              length: -15, // 便宜的长度
              lineStyle: {
                color: '#fff'
              }
            } // 分隔线样式
          },
          {
            type: 'gauge', // 刻度轴表盘
            radius: '100%', // 刻度盘的大小
            center: ['50%', '50%'], // 刻度盘的位置
            max: this.vmax,
            splitNumber: 5, // 刻度数量
            startAngle: 225, // 开始刻度的角度
            endAngle: -45, // 结束刻度的角度
            axisLine: {
              // 刻度的线条
              show: true,
              lineStyle: {
                width: 10, // 定义一个宽15的数轴
                color: [
                  // 颜色为渐变色
                  [
                    this.value / this.vmax,
                    new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
                      {
                        offset: 0,
                        color: '#d2ef19'
                      },
                      {
                        offset: 1,
                        color: '#cb1344'
                      }
                    ])
                  ],
                  [1, '#413e54']
                ]
              }
            },
            // 分隔线样式。
            splitLine: {
              // 表盘上的轴线
              show: false
            },
            axisLabel: {
              // 表盘上的刻度数值文字
              show: false
            },
            axisTick: {
              // 表盘上的刻度线
              show: false
            },
            pointer: {
              // 表盘上的指针
              show: true
            },
            itemStyle: {
              // 表盘指针的颜色
              color: '#18c8ff'
            },
            title: {
              // 标题
              show: true,
              offsetCenter: [0, '80%'], // x, y，单位px
              textStyle: {
                color: '#efc253',
                fontSize: 14 // 表盘上的标题文字大小
              }
            },
            // 仪表盘详情，用于显示数据。
            detail: {
              show: true,
              offsetCenter: [0, '55%'],
              color: '#366cc0',
              formatter: function(params) {
                if (parseFloat(params) > 5) {
                  return '超重啦！'
                } else { return params + 'kg' }
              },
              textStyle: {
                fontSize: 14
              }
            },
            data: [
              // 当前数值的数据
              {
                name: '当前负载重量',
                value: this.value
              }
            ]
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
      deep: true
    }
  },
  mounted() {
    this.chart = this.$echarts.init(this.$refs.chartFieldRef)
    this.chart.setOption(this.option)
  }
}
</script>

<style scoped>

</style>

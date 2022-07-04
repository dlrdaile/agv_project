<template>
  <div class="rosheader-container">
    <!--    页面标题栏-->
    <el-row class="title">
      <!--页面左侧选项栏-->
      <el-col
        :span="6"
      >
        <dv-decoration-10
          class="title_left"
          :color="['#008CFF', '#00ADDD']"
        />
      </el-col>
      <!--页面中间标题-->
      <el-col
        :span="12"
      >
        <div class="title_text">数 据 可 视 化 系 统</div>
        <dv-decoration-5
          class="title_center"
          :color="['#008CFF', '#00ADDD']"
          :dur="5"
        />
      </el-col>
      <!--页面右侧状态栏-->
      <el-col :span="6">
        <div class="right-items">
          <span class="title_time">{{ [dateYear, dateWeek, dateDay].join('  ') }}</span>

          <img class="signal" src="@/assets/images/signal.png" @click="click">
          <span class="battery">
            <dv-percent-pond :config="config" style="width:70px;height:30px;" />
          </span>
          <el-badge is-dot class="item status-icon">
            <el-link
              type="primary"
              :underline="false"
              icon="el-icon-s-opportunity"
            >正常
            </el-link>
          </el-badge>
          <flash-icon v-if="isCharge" class="flash-icon" />
        </div>
        <dv-decoration-10
          :reverse="true"
          class="title_right"
          :color="['#008CFF', '#00ADDD']"
        />
      </el-col>
    </el-row>
    <!--    主页面区-->

  </div>
</template>

<script>
import FlashIcon from '@/views/rosPanel/component/FlashIcon'
export default {
  name: 'RosPanelHeader',
  components: {
    FlashIcon
  },
  data() {
    return {
      activeIndex: '1',
      activeIndex2: '1',
      isCharge: true,
      // 时分秒
      dateDay: null,
      // 年月日
      dateYear: null,
      // 周几
      dateWeek: null,
      timing: null,
      weekday: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
      config: {
        value: 0,
        lineDash: [10, 2],
        // localGradient: true,
        colors: ['#d2142a', '#dc8717', '#67d20e'],
        formatter: '未 连 接'
      }
    }
  },
  watch: {
    isCharge: function(n, o) {
      if (n) {
        this.config.formatter = '{value}%'
        this.config.value = 50
      }
    }
  },
  beforeDestroy() {
    // 离开时删除计时器
    clearInterval(this.timing)
  },
  mounted() {
    // 获取实时时间
    this.timeFn()
  },
  methods: {
    click() {
      console.log(1)
    },
    timeFn() {
      this.timing = setInterval(() => {
        // 获取当前时分秒
        this.dateDay = this.formatTime(new Date(), 'HH: mm: ss')
        // 获取当前年月日
        this.dateYear = this.formatTime(new Date(), 'yyyy-MM-dd')
        // 获取当前周几
        this.dateWeek = this.weekday[new Date().getDay()]
      }, 1000)
    },
    /**
     * @param {date} time 需要转换的时间
     * @param {String} fmt 需要转换的格式 如 yyyy-MM-dd、yyyy-MM-dd HH:mm:ss
     */
    formatTime(time, fmt) {
      if (!time) return ''// 没传时间返回空
      else {
        const date = new Date(time)
        const o = {
          'M+': date.getMonth() + 1, // 月
          'd+': date.getDate(), // 日
          'H+': date.getHours(), // 时
          'm+': date.getMinutes(), // 分
          's+': date.getSeconds(), // 秒
          'q+': Math.floor((date.getMonth() + 3) / 3), // 月+3/3
          S: date.getMilliseconds()// 返回时间的毫秒
        }
        if (/(y+)/.test(fmt))// 匹配1个到多个y
        // 这一步把年转换完毕
        // eslint-disable-next-line brace-style
        {
          fmt = fmt.replace(
            RegExp.$1, // 拿到y+匹配到的第一个分组
            (date.getFullYear() + '').substr(4 - RegExp.$1.length)
          )
        }
        // 这一步把生下的格式继续匹配转换
        for (const k in o) {
          if (new RegExp('(' + k + ')').test(fmt)) {
            fmt = fmt.replace(
              RegExp.$1,
              RegExp.$1.length === 1
                ? o[k]
                : ('00' + o[k]).substr(('' + o[k]).length)
            )
          }
        }
        return fmt
      }
    }
  }
}
</script>

<style scoped lang="scss">
.rosheader-container {
  position: absolute;
  width: 100%;
  .title {
    .title_right {
      width: 100%;
      height: 50px;
      margin-top: 18px;
    }

    //顶部左边装饰效果
    .title_left {
      width: 100%;
      height: 50px;
      margin-top: 18px;
    }

    //顶部中间装饰效果
    .title_center {
      width: 100%;
      height: 50px;
    }

    //顶部中间文字数据可视化系统
    .title_text {
      text-align: center;
      font-size: 24px;
      font-weight: bold;
      margin-top: 14px;
      color: #008cff;
    }

    .left-items {
      position: absolute;
      height: 40px;
      background-color: transparent;

      li {
        height: 100%;
      }
    }

    .right-items {
      position: relative;

      .battery {
        position: absolute;
        padding-top: 10px;
        right: 7%;

        ::v-deep text {
          font-size: 13px;
        }

      }

      .signal {
        position: absolute;
        width: 30px;
        height: 40px;
        padding-top: 10px;
        left: 45%;
        cursor: pointer;
      }

      .flash-icon {
        position: absolute;
        transform: translateX(1800%);
        width: 10px;
        height: 40px;
        margin-top: 20px;
      }

      .title_time {
        font-size: 10px;
        position: absolute;
        padding-top: 15px;
        color: white;
        left: 1%;
      }

      .status-icon {
        position: absolute;
        left: 57%;
        padding-top: 6px;
        margin-top: 8px;
      }
    }
  }
}
</style>

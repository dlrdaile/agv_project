<template>
  <div id="app">
    <div class="container">
      <el-col :span="6" class="choose-item">
        <el-radio-group v-model="radio1" class="choose-container" @change="getChange">
          <el-radio-button label="login" class="login">
            <div class="login-main">
              <i class="el-icon-user-solid" style="font-size: x-large" />
              <h2>登录</h2>
            </div>
          </el-radio-button>
          <el-radio-button label="register" class="register">
            <div class="register-main">
              <i class="el-icon-edit" style="font-size: x-large" />
              <h2>注册</h2>
            </div>
          </el-radio-button>
          <el-radio-button label="forget" class="forget">
            <div class="forget-main">
              <i class="el-icon-lock" style="font-size: x-large" />
              <h2>忘记密码</h2>
            </div>
          </el-radio-button>
        </el-radio-group>
      </el-col>
      <el-col :span="18" class="main">
        <div class="header">
          <span>
            <img src="../../assets/images/R-C.png" alt="" style="width: 40px;height: 40px;">
            <!--            <el-avatar src="@/assets/images/R-C.png">agv</el-avatar>-->
          </span>
          AGV调度软件
        </div>
        <el-card class="content">
          <keep-alive>
            <component
              :is="main_comp"
              @compRegister="redirectRegister"
            />
          </keep-alive>
        </el-card>
      </el-col>
    </div>
  </div>
</template>

<script>
import Login from '@/components/login'
import Register from '@/components/register'
import Forget from '@/components/forget'

export default {
  components: {
    Login,
    Register,
    Forget
  },
  data() {
    return {
      radio1: 'login',
      main_comp: 'login',
      redirect: undefined
    }
  },
  methods: {
    redirectRegister() {
      this.main_comp = 'login'
      this.radio1 = 'login'
    },
    getChange(chooseItem) {
      this.main_comp = chooseItem
    }
  }
}
</script>

<style scoped lang="scss">
#app {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: url("https://img95.699pic.com/photo/40034/4174.jpg_wh860.jpg");
  background-color: #fff;
  background-repeat: no-repeat;
  background-size: cover;

  -webkit-background-size: cover;

  -o-background-size: cover;

  background-position: center 0;

  .container {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 650px;
    height: 500px;
    opacity: 0.85;

    .choose-item {
      height: 100%;
    }

    .main {
      height: 100%;
      display: grid;
      grid-auto-rows: 1fr 3fr;

      .header {
        border-bottom: 2px solid white;
        text-align: center;
        font-size: 40px;
        padding-top: 30px;
        background: none;
        font-family: GEETYPE歌留多丸体大粗;
        background-color: white;
      }

      .content {
        background-color: white;
      }
    }

    .choose-container {
      display: grid;
      height: 100%;
      grid-template-columns: 1fr;
      grid-template-rows: repeat(3, 1fr);
      gap: 0px 0px;
      grid-auto-flow: row;
      grid-template-areas:
    "login"
    "register"
    "forget";

      .login {
        grid-area: login;
        background-color: chartreuse;

        > span {
          width: 100px;
        }
      }

      .register {
        grid-area: register;
        background-color: antiquewhite;
      }

      .forget {
        grid-area: forget;
        background-color: blueviolet;
      }
    }
  }

::v-deep span.el-radio-button__inner {
    display: block;
    height: 100%;
    position: relative;
    padding: 0;

    div {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);

      i {
        margin-bottom: 10px;
        font-size: 20px;
      }

      h2 {
        font-size: 15px;
      }
    }

    .login-main {
    }

    .register-main {
    }

    .forget-main {
    }
  }
}

::v-deep .bottom-position {
  text-align: right;
  position: absolute;
  bottom: 5%;
  right: 5%;
}

</style>

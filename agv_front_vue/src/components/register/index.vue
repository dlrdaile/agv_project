<template>
  <div id="register-container">
    <el-steps :active="active" finish-status="success">
      <el-step title="账号信息" />
      <el-step title="用户信息" />
      <el-step title="邮箱校验" />
    </el-steps>
    <el-form
      ref="registerForm"
      :model="registerForm"
      status-icon
      :rules="rules"
      label-width="70px"
      style="margin-top: 30px"
      label-position="left"
    >
      <!--      账号信息-->
      <el-form-item v-show="active === 0" label="用户" prop="username">
        <el-input
          v-model="registerForm.username"
          type="text"
          prefix-icon="el-icon-user-solid"
          :clearable="true"
        />
      </el-form-item>
      <el-form-item v-show="active === 0" label="密码" prop="password">
        <el-input
          v-model="registerForm.password"
          type="password"
          autocomplete="off"
          :clearable="true"
          prefix-icon="el-icon-lock"
        />
      </el-form-item>
      <el-form-item v-show="active === 0" label="确认密码" prop="checkPass">
        <el-input
          v-model="registerForm.checkPass"
          type="password"
          :clearable="true"
          prefix-icon="el-icon-lock"
          autocomplete="off"
        />
      </el-form-item>

      <!--      用户信息-->
      <el-form-item v-show="active === 1" label="昵称" prop="nickname">
        <el-input
          v-model="registerForm.nickname"
          type="text"
          prefix-icon="el-icon-user"
          :clearable="true"
        />
      </el-form-item>
      <el-form-item v-show="active === 1" label="电话" prop="phone">
        <el-input
          v-model="registerForm.phone"
          type="text"
          :clearable="true"
          prefix-icon="el-icon-phone"
          autocomplete="off"
        />
      </el-form-item>
      <el-form-item v-show="active === 1" label="地址" prop="address">
        <el-cascader
          v-model="registerForm.address"
          filterable
          :options="options"
          clearable
        />
      </el-form-item>

      <!--      邮箱校验-->
      <el-form-item
        v-show="active === 2"
        label="邮箱"
        prop="email"
        :rules="[
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }]"
      >
        <el-col :span="18">
          <el-input
            v-model="registerForm.email"
            prefix-icon="el-icon-message"
            placeholder="输入邮箱并点击发送验证码"
          />
        </el-col>
        <el-button
          :loading="codeLoading"
          :disabled="isDisable"
          size="small"
          round
          @click="sendMsg"
        >发送验证码
        </el-button>
        <span style="float: left">{{ statusMsg }}</span>
      </el-form-item>
      <el-form-item v-show="active === 2" label="验证码" prop="code">
        <el-col :span="18">
          <el-input
            v-model="registerForm.code"
            auto-complete="off"
            prefix-icon="el-icon-bell"
            maxlength="6"
            placeholder="请输入邮箱中的验证码"
          />
        </el-col>
      </el-form-item>
      <span v-show="active === 3">恭喜你完成了信息输入，请点击注册按钮进行注册吧!</span>

      <!--      提交按钮-->
      <el-form-item class="bottom-position">
        <el-button v-show="active!==0" type="primary" @click="lastStep">上一步</el-button>
        <el-button type="primary" @click="nextStep">{{ buttonText }}</el-button>
      </el-form-item>

    </el-form>
  </div>
</template>

<script>
import { getEmailCode } from '@/api/emails'
import { register } from '@/api/user'

export default {
  name: 'Register',
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.registerForm.checkPass !== '') {
          this.$refs.registerForm.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.registerForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      statusMsg: '',
      options: [],
      registerForm: {
        password: '',
        checkPass: '',
        username: '',
        phone: '',
        nickname: '',
        address: '',
        email: '',
        code: ''
      },
      active: 0,
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
          { validator: validatePass2, trigger: 'blur' }
        ],
        nickname: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { min: 11, max: 11, message: '请输入11位手机号码', trigger: 'blur' },
          {
            pattern: /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/,
            message: '请输入正确的手机号码'
          }
        ]
      },
      codeLoading: false,
      isDisable: false
    }
  },
  computed: {
    buttonText() {
      if (this.active === 3) return '注册'
      else return '下一步'
    }
  },
  created() {
    this.getMapList()
  },
  methods: {
    async getMapList() {
      const { data: res } = await this.$store.dispatch('map/GetMapList')
      this.options = res
      this.$store.commit('map/SET_MAPLIST', res)
    },
    nextStep() {
      if (this.active === 3) {
        const that = this
        this.$refs.registerForm.validate((valid) => {
          if (valid) {
            const loading = that.$loading({
              lock: true,
              text: '正在注册',
              spinner: 'el-icon-loading',
              background: 'rgba(0, 0, 0, 0.7)'
            })
            var request_data = { ...that.registerForm }
            request_data.name = request_data.username
            register(request_data).then(
              () => {
                that.$message.success('注册成功！')
                loading.close()
                that.active = 0
                that.$emit('redirectToLogin')
              }
            ).catch(() => {
              loading.close()
            })
          }
        })
      } else {
        this.active++
      }
    },
    lastStep() {
      this.active -= 1
    },
    sendMsg() {
      const self = this
      let emailPass
      let timerid
      if (timerid) {
        return false
      }
      self.statusMsg = ''
      this.$refs['registerForm'].validateField('email', (valid) => {
        emailPass = valid
      })
      // 向后台API验证码发送
      if (!emailPass) {
        self.codeLoading = true
        self.statusMsg = '验证码发送中...'
        getEmailCode(self.registerForm.email, 'register').then(res => {
          this.$message({
            showClose: true,
            message: '发送成功，验证码有效期5分钟',
            type: 'success'
          })
          let count = 60
          self.registerForm.code = ''
          self.codeLoading = false
          self.isDisable = true
          self.statusMsg = `验证码已发送,${count--}秒后重新发送`
          timerid = window.setInterval(function() {
            self.statusMsg = `验证码已发送,${count--}秒后重新发送`
            if (count <= 0) {
              window.clearInterval(timerid)
              self.isDisable = false
              self.statusMsg = ''
            }
          }, 1000)
        }).catch(err => {
          console.log(err)
          this.isDisable = false
          this.statusMsg = ''
          this.codeLoading = false
        })
      }
    }
  }
}
</script>

<style scoped lang="scss">
#register-container {

}
</style>

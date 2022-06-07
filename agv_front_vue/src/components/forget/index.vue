<template>
  <div class="forget-container">
    <el-form
      ref="forgetForm"
      :model="forgetForm"
      status-icon
      :rules="rules"
      label-width="70px"
      style="margin-top: 20px"
      label-position="left"
    >
      <el-form-item
        label="邮箱"
        prop="email"
        :rules="[
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }]"
      >
        <el-col :span="18">
          <el-input
            v-model="forgetForm.email"
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
      <el-form-item label="验证码" prop="code">
        <el-col :span="18">
          <el-input
            v-model="forgetForm.code"
            prefix-icon="el-icon-bell"
            maxlength="6"
            placeholder="请输入邮箱中的验证码"
            auto-complete="off"
          />
        </el-col>
      </el-form-item>
      <el-form-item label="新密码" prop="new_password">
        <el-col :span="18">
          <el-input
            v-model="forgetForm.new_password"
            type="password"
            autocomplete="off"
            :clearable="true"
            prefix-icon="el-icon-lock"
          />
        </el-col>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-col :span="18">
          <el-input
            v-model="forgetForm.checkPass"
            type="password"
            :clearable="true"
            prefix-icon="el-icon-lock"
            autocomplete="off"
          />
        </el-col>
      </el-form-item>

      <el-form-item class="bottom-position">
        <el-button type="primary" @click="submitForm('forgetForm')">提交</el-button>
        <el-button @click="$refs.forgetForm.resetFields()">重置</el-button>
      </el-form-item>
    </el-form>
  </div>

</template>

<script>
import { getEmailCode } from '@/api/emails'
import { forget } from '@/api/user'

export default {
  name: 'Forget',
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.forgetForm.checkPass !== '') {
          this.$refs.forgetForm.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.forgetForm.new_password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      forgetForm: {
        email: '',
        code: '',
        new_password: '',
        checkPass: ''
      },
      codeLoading: false,
      isDisable: false,
      statusMsg: '',
      rules: {
        new_password: [
          { validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
          { validator: validatePass2, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    sendMsg() {
      const self = this
      let emailPass
      let timerid
      if (timerid) {
        return false
      }
      self.statusMsg = ''
      this.$refs['forgetForm'].validateField('email', (valid) => {
        emailPass = valid
      })
      // 向后台API验证码发送
      if (!emailPass) {
        self.codeLoading = true
        self.statusMsg = '验证码发送中...'
        getEmailCode(self.forgetForm.email, 'forget').then(res => {
          this.$message({
            showClose: true,
            message: '发送成功，验证码有效期5分钟',
            type: 'success'
          })
          let count = 60
          self.forgetForm.code = ''
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
    },
    submitForm() {
      const that = this
      this.$refs.forgetForm.validate((valid) => {
        if (valid) {
          const loading = that.$loading({
            lock: true,
            text: '正在注册',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          })
          const request_data = {
            'new_password': {
              'password': that.forgetForm.new_password
            },
            'validData': {
              'email': that.forgetForm.email,
              'valid_code': that.forgetForm.code
            }
          }
          forget(request_data).then(
            () => {
              this.$message.success('密码修改成功！')
              loading.close()
              that.$emit('redirectToLogin')
            }
          ).catch(() => {
            loading.close()
          })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>

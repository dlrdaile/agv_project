<template>
  <div class="forget-container">
    <el-form
      ref="ruleForm"
      :model="forgetForm"
      status-icon
      :rules="rules"
      label-width="70px"
      class="demo-ruleForm"
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
        <span class="status">{{ statusMsg }}</span>
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
      <el-form-item label="新密码" prop="password">
        <el-col :span="18">
          <el-input
            v-model="forgetForm.password"
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
        <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button @click="$refs.ruleForm.resetFields()">重置</el-button>
      </el-form-item>
    </el-form>
  </div>

</template>

<script>
export default {
  name: 'Forget',
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.forgetForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.forgetForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      forgetForm: {
        email: '',
        code: '',
        password: '',
        checkPass: ''
      },
      codeLoading: false,
      isDisable: false,
      statusMsg: '',
      rules: {
        password: [
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
      this.$refs['ruleForm'].validateField('email', (valid) => {
        emailPass = valid
      })
      // 向后台API验证码发送
      if (!emailPass) {
        self.codeLoading = true
        self.statusMsg = '验证码发送中...'
        // getEmailCode(self.ruleForm.email).then(res => {
        //   this.$message({
        //     showClose: true,
        //     message: '发送成功，验证码有效期5分钟',
        //     type: 'success'
        //   })
        //   let count = 60
        //   self.ruleForm.code = ''
        //   self.codeLoading = false
        //   self.isDisable = true
        //   self.statusMsg = `验证码已发送,${count--}秒后重新发送`
        //   timerid = window.setInterval(function() {
        //     self.statusMsg = `验证码已发送,${count--}秒后重新发送`
        //     if (count <= 0) {
        //       window.clearInterval(timerid)
        //       self.isDisable = false
        //       self.statusMsg = ''
        //     }
        //   }, 1000)
        // }).catch(err => {
        //   this.isDisable = false
        //   this.statusMsg = ''
        //   this.codeLoading = false
        //   console.log(err.response.data.message)
        // })
      }
    },
    submitForm() {

    }
  }
}
</script>

<style scoped>

</style>

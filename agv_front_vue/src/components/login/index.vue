<template>
  <div class="login-container">
    <el-form
      ref="ruleForm"
      :model="loginForm"
      status-icon
      :rules="rules"
      label-width="80px"
      class="demo-ruleForm"
      style="margin-top: 80px"
      label-position="left"
    >
      <el-form-item label="用户" prop="username">
        <el-input
          v-model="loginForm.username"
          type="text"
          autocomplete="on"
          :placeholder="'admin or email'"
          prefix-icon="el-icon-user-solid"
        />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          v-model="loginForm.password"
          type="password"
          autocomplete="on"
          :show-password="true"
          placeholder="password"
          prefix-icon="el-icon-lock"
        />
      </el-form-item>
      <el-form-item class="bottom-position">
        <el-button :loading="loading" type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button @click="$refs.ruleForm.resetFields()">重置</el-button>
      </el-form-item>

    </el-form>
    <Vcode :show="isShow" @success="success" @close="close" />
  </div>
</template>

<script>
import Vcode from 'vue-puzzle-vcode'

export default {
  name: 'Login',
  components: {
    Vcode
  },
  data() {
    return {
      isShow: false,
      loginForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.isShow = true
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    success(msg) {
      this.isShow = false // 通过验证后，需要手动隐藏模态框
      this.loading = true
      this.$store
        .dispatch('user/login', this.loginForm)
        .then(() => {
          this.$router.push({ path: '/' })
          // this.$router.push({ path: this.redirect || '/' })
          this.loading = false
        })
        .catch(() => {
          this.loading = false
        })
    },
    // 用户点击遮罩层，应该关闭模态框
    close() {
      this.isShow = false
    }
  }
}
</script>

<style scoped>

</style>

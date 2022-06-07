<template>
  <div id="register-container">
    <el-steps :active="active" finish-status="success">
      <el-step title="账号信息" />
      <el-step title="用户信息" />
      <el-step title="邮箱校验" />
    </el-steps>
    <el-form
      ref="ruleForm"
      :model="registerForm"
      status-icon
      :rules="rules"
      label-width="70px"
      class="demo-ruleForm"
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
        <span class="status">{{ statusMsg }}</span>
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
export default {
  name: 'Register',
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.registerForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
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
      options: [{
        value: 'zhinan',
        label: '指南',
        children: [{
          value: 'shejiyuanze',
          label: '设计原则',
          children: [{
            value: 'yizhi',
            label: '一致'
          }, {
            value: 'fankui',
            label: '反馈'
          }, {
            value: 'xiaolv',
            label: '效率'
          }, {
            value: 'kekong',
            label: '可控'
          }]
        }, {
          value: 'daohang',
          label: '导航',
          children: [{
            value: 'cexiangdaohang',
            label: '侧向导航'
          }, {
            value: 'dingbudaohang',
            label: '顶部导航'
          }]
        }]
      }, {
        value: 'zujian',
        label: '组件',
        children: [{
          value: 'basic',
          label: 'Basic',
          children: [{
            value: 'layout',
            label: 'Layout 布局'
          }, {
            value: 'color',
            label: 'Color 色彩'
          }, {
            value: 'typography',
            label: 'Typography 字体'
          }, {
            value: 'icon',
            label: 'Icon 图标'
          }, {
            value: 'button',
            label: 'Button 按钮'
          }]
        }, {
          value: 'form',
          label: 'Form',
          children: [{
            value: 'radio',
            label: 'Radio 单选框'
          }, {
            value: 'checkbox',
            label: 'Checkbox 多选框'
          }, {
            value: 'input',
            label: 'Input 输入框'
          }, {
            value: 'input-number',
            label: 'InputNumber 计数器'
          }, {
            value: 'select',
            label: 'Select 选择器'
          }, {
            value: 'cascader',
            label: 'Cascader 级联选择器'
          }, {
            value: 'switch',
            label: 'Switch 开关'
          }, {
            value: 'slider',
            label: 'Slider 滑块'
          }, {
            value: 'time-picker',
            label: 'TimePicker 时间选择器'
          }, {
            value: 'date-picker',
            label: 'DatePicker 日期选择器'
          }, {
            value: 'datetime-picker',
            label: 'DateTimePicker 日期时间选择器'
          }, {
            value: 'upload',
            label: 'Upload 上传'
          }, {
            value: 'rate',
            label: 'Rate 评分'
          }, {
            value: 'form',
            label: 'Form 表单'
          }]
        }, {
          value: 'data',
          label: 'Data',
          children: [{
            value: 'table',
            label: 'Table 表格'
          }, {
            value: 'tag',
            label: 'Tag 标签'
          }, {
            value: 'progress',
            label: 'Progress 进度条'
          }, {
            value: 'tree',
            label: 'Tree 树形控件'
          }, {
            value: 'pagination',
            label: 'Pagination 分页'
          }, {
            value: 'badge',
            label: 'Badge 标记'
          }]
        }, {
          value: 'notice',
          label: 'Notice',
          children: [{
            value: 'alert',
            label: 'Alert 警告'
          }, {
            value: 'loading',
            label: 'Loading 加载'
          }, {
            value: 'message',
            label: 'Message 消息提示'
          }, {
            value: 'message-box',
            label: 'MessageBox 弹框'
          }, {
            value: 'notification',
            label: 'Notification 通知'
          }]
        }, {
          value: 'navigation',
          label: 'Navigation',
          children: [{
            value: 'menu',
            label: 'NavMenu 导航菜单'
          }, {
            value: 'tabs',
            label: 'Tabs 标签页'
          }, {
            value: 'breadcrumb',
            label: 'Breadcrumb 面包屑'
          }, {
            value: 'dropdown',
            label: 'Dropdown 下拉菜单'
          }, {
            value: 'steps',
            label: 'Steps 步骤条'
          }]
        }, {
          value: 'others',
          label: 'Others',
          children: [{
            value: 'dialog',
            label: 'Dialog 对话框'
          }, {
            value: 'tooltip',
            label: 'Tooltip 文字提示'
          }, {
            value: 'popover',
            label: 'Popover 弹出框'
          }, {
            value: 'card',
            label: 'Card 卡片'
          }, {
            value: 'carousel',
            label: 'Carousel 走马灯'
          }, {
            value: 'collapse',
            label: 'Collapse 折叠面板'
          }]
        }]
      }, {
        value: 'ziyuan',
        label: '资源',
        children: [{
          value: 'axure',
          label: 'Axure Components'
        }, {
          value: 'sketch',
          label: 'Sketch Templates'
        }, {
          value: 'jiaohu',
          label: '组件交互文档'
        }]
      }],
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
  methods: {
    nextStep() {
      if (this.active++ > 2) {
        this.active = 0
        this.$emit('compRegister')
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
      this.$refs['ruleForm'].validateField('email', (valid) => {
        emailPass = valid
      })
      // 向后台API验证码发送
      if (!emailPass) {
        self.codeLoading = true
        self.statusMsg = '验证码发送中...'
        /*        getEmailCode(self.ruleForm.email).then(res => {
          this.$message({
            showClose: true,
            message: '发送成功，验证码有效期5分钟',
            type: 'success'
          })
          let count = 60
          self.ruleForm.code = ''
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
          this.isDisable = false
          this.statusMsg = ''
          this.codeLoading = false
          console.log(err.response.data.message)
        })*/
      }
    }
  }
}
</script>

<style scoped lang="scss">
#register-container {

}
</style>

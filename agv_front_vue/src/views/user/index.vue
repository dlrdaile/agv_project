<template>
  <div class="users">
    <el-card class="box-card">
      <el-row :gutter="20">
        <el-col :span="7">
          <!-- 搜索与添加区域 -->
          <el-input v-model="queryInfo.query" placeholder="请输入内容" clearable @clear="getUserList">
            <el-button
              slot="append"
              type="primary"
              icon="el-icon-search"
              @click="getUserList"
            />
          </el-input>
        </el-col>
      </el-row>
      <el-table
        :data="userData.userList"
        border
        stripe
        highlight-current-row
      >
        <el-table-column type="expand">
          <template v-slot="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="ID:">
                <span>{{ props.row.id }}</span>
              </el-form-item>
              <el-form-item label="用户名:">
                <span>{{ props.row.nickname }}</span>
              </el-form-item>
              <el-form-item label="邮箱:">
                <span>{{ props.row.email }}</span>
              </el-form-item>
              <el-form-item label="手机号:">
                <span>{{ props.row.phone }}</span>
              </el-form-item>
              <el-form-item label="地址:">
                <span>{{ props.row.address }}</span>
              </el-form-item>
              <el-form-item label="创建时间:">
                <span>{{ parseTime(props.row.create_time) }}</span>
              </el-form-item>
              <el-form-item label="上次登录时间">
                <span>{{ parseTime(props.row.last_active_time) }}</span>
              </el-form-item>
              <el-form-item label="是否活跃">
                <span v-if="props.row.isActive==false"><font color="#E6A23C">不活跃</font></span>
                <span v-else><font color="#67C23A">活跃中</font></span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="ID"
          prop="id"
          width="80"
          align="center"
        >
          <template v-slot="props">
            <span>{{ props.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="用户名"
          prop="nickname"
          align="center"
        >
          <template v-slot="props">
            <span>{{ props.row.nickname }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="邮箱"
          prop="email"
          align="center"
        >
          <template v-slot="props">
            <span>{{ props.row.email }}</span>
          </template></el-table-column>
        <el-table-column
          label="手机号"
          prop="phone"
          align="center"
        >
          <template v-slot="props">
            <span>{{ props.row.phone }}</span>
          </template></el-table-column>
        <el-table-column
          label="是否活跃"
          prop="isActive"
          align="center"
        >
          <template v-slot="props">
            <el-button v-if="props.row.isActive==true" type="success" size="mini">活跃中</el-button>
            <el-button v-else type="warning" size="mini">不活跃</el-button>
          </template></el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        :current-page="queryInfo.pagenum"
        :page-size="queryInfo.pagesize"
        :page-sizes="[5, 9, 13, 15]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="userData.total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </el-card>
  </div>
</template>

<script>
import { parseTime } from '@/utils'

export default {
  data() {
    return {
      // 获取用户列表的参数对象
      queryInfo: {
        // 搜索值
        query: '',
        // 当前的页数
        pagenum: 1,
        // 当前每次显示多少条数据
        pagesize: 5
      },
      // 存放用户的数据和数量
      userData: {
        userList: [
          { id: 1,
            email: 'sdafsdfsdfas',
            phone: 121212121212,
            address: 'sdfdasfasd',
            nickname: '我是大傻子',
            create_time: '1335205592410',
            last_active_time: 'sadfsdaf',
            isActive: false
          },
          { id: 2,
            email: 'sdafsdfsdfas',
            phone: 121212121212,
            address: 'sdfdasfasd',
            nickname: '我是大傻子',
            create_time: 'asdfsdaf',
            last_active_time: 'sadfsdaf',
            isActive: true
          }

        ],
        total: 0
      },
      // 添加用户数据的对象
      addForm: {
        username: '',
        password: '',
        email: '',
        mobile: ''
      },
      selectRoleId: '',
      // 查询用户的对象
      editForm: {}
    }
  },
  created() {
    this.getUserList()
  },
  methods: {
    parseTime(value) {
      return parseTime(Date.parse(value), '{y}-{m}-{d} {h}:{i}')
    },
    /* 布尔值格式化：cellValue为后台返回的值*/
    isActiveFiltter: function(row, column, isActive) {
      var ret = '' // 你想在页面展示的值
      if (isActive) {
        ret = '活跃中' // 根据自己的需求设定
      } else {
        ret = '不活跃'
      }
      return ret
    },
    async getUserList() {
      const { data: res } = await this.$http.get('users', {
        params: this.queryInfo
      })
      if (res.meta.status !== 200) {
        this.$message.error('获取用户列表失败!')
      }
      this.$message.success('获取用户列表成功!')
      this.userData.userList = res.data.users
      this.userData.total = res.data.total
      // console.log(res)
    },
    // 监听 pagesize 改变事件 每页显示的个数
    handleSizeChange(newSize) {
      // console.log(newSize)
      this.queryInfo.pagesize = newSize
      this.getUserList()
    },
    // 监听 页码值 改变的事件 当前页面值
    handleCurrentChange(newPage) {
      console.log(newPage)
      this.queryInfo.pagenum = newPage
      this.getUserList()
    }
  }

}
</script>

<style lang="scss" scoped>
.el-table {
  margin-top: 15px;
}
.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 25%;
}
</style>

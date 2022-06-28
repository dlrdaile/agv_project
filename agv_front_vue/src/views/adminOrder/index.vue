<template>
  <div class="app-container">
    <div class="filter-container">
      <!--      搜索区-->
      <!--      通过ID排序-->
      <el-select v-model="listQuery.desc" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <!--      通过零件搜索-->
      <el-select
        v-model="listQuery.item_id"
        placeholder="零件名"
        clearable
        class="filter-item"
        style="width: 130px"
        filterable
        multiple
        collapse-tags
        @change="handleFilter"
      >
        <el-option-group
          v-for="(group,key) in item_list"
          :key="key"
          :label="key"
        >
          <el-option
            v-for="item in group"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-option-group>
      </el-select>
      <!--      通过用户名筛选-->
      <el-select
        v-model="listQuery.user_id"
        placeholder="用户名"
        clearable
        class="filter-item"
        style="width: 130px"
        filterable
        multiple
        collapse-tags
        @change="handleFilter"
      >
        <el-option
          v-for="item in user_list"
          :key="item.id"
          :label="item.name"
          :value="item.id"
        />
      </el-select>
      <!--      通过零件处理状态搜索-->
      <el-select
        v-model="listQuery.orderState"
        multiple
        style="width: 140px"
        class="filter-item"
        @change="handleFilter"
      >
        <el-option v-for="item in orderStatusOption" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <!--      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">-->
      <!--        搜索-->
      <!--      </el-button>-->
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"
        icon="el-icon-edit"
        @click="handleCreate"
      >
        增加
      </el-button>
      <!-- <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        输出 EXCEL
      </el-button> -->
    </div>
    <!--表格区-->
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="userOrderList"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column
        label="ID"
        prop="id"
        sortable="custom"
        align="center"
        width="80"
      >
        <!--        <template v-slot="{$index}">-->
        <!--          <span>{{ getOrderId($index) }}</span>-->
        <!--        </template>        -->
        <template v-slot="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" prop="time" sortable="custom" width="150px" align="center">
        <template v-slot="{row}">
          <span>{{ parseTime(row.create_time) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="订单名" min-width="80px" align="center">
        <template v-slot="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="零件名" width="80" align="center">
        <template v-slot="{row}">
          <span>{{ row.item_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="用户" width="80" align="center">
        <template v-slot="{row}">
          <span class="link-type" @click="handlegetUserData(row.user_id)">{{ row.user_name }}</span>
        </template>
      </el-table-column>
      <!-- 判断订单状态，当为非草稿状态时，渲染已完成等 -->
      <el-table-column label="订单状态" align="center">
        <template v-slot="{row}">
          <span>
            <el-button
              round
              :type="processStatus(row.status)[0]"
              size="mini"
            >{{ processStatus(row.status)[1] }}<el-popover
              v-if="processStatus(row.status)[0] === 'danger'"
              placement="top-start"
              title="错误原因"
              width="200"
              trigger="hover"
              :content="row.reject_or_fail_reason"
            ><i class="el-icon-s-opportunity el-icon--right" />
            </el-popover>
            </el-button>
          </span>
        </template>
      </el-table-column>
      <el-table-column label="处理" align="center" min-width="260px" class-name="small-padding fixed-width">
        <template v-slot="{row}">
          <el-button :disabled="row.status == 1 || row.status == 3 || row.status == 4" type="primary" size="mini" @click="handleAccept(row)">
            接受
          </el-button>
          <el-button :disabled="row.status == 2 || row.status == 1 || row.status == 4" size="mini" type="danger" @click="dialogRejectVisible = true">
            拒绝
          </el-button>
          <el-button
            :disabled="row.status === 1"
            size="mini"
            type="danger"
            @click="handleDelete(row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--分页区-->
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getOrderList"
    />
    <!--动态展示的dialog-->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="addOrderForm"
        label-position="left"
        label-width="70px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="订单名" prop="name">
          <el-input v-model="addOrderForm.name" />
        </el-form-item>
        <el-form-item label="选择商品" prop="item_id">
          <el-select v-model="addOrderForm.item_id" class="filter-item" placeholder="请选择" clearable filterable>
            <el-option-group
              v-for="(group,key) in item_list"
              :key="key"
              :label="key"
            >
              <el-option
                v-for="item in group"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-option-group>
          </el-select>
        </el-form-item>
        <el-form-item label="备注信息" prop="description">
          <el-input v-model="addOrderForm.description" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="请输入" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>

    <!--拒绝对话框-->
    <el-dialog
      title="拒绝订单原因"
      :visible.sync="dialogRejectVisible"
      width="30%"
    >
      <el-input
        v-model="rejectReason"
        type="textarea"
        :rows="2"
        placeholder="请输入拒绝原因"
      />
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogRejectVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleReject(row)">确 定</el-button>
      </span>
    </el-dialog>
    <!--用户信息对话框-->
    <el-dialog :visible.sync="dialogUserVisible" title="用户信息">
      <el-descriptions>
        <el-descriptions-item label="用户名">{{ userData.name }}</el-descriptions-item>
        <el-descriptions-item label="手机号">18100000000</el-descriptions-item>
        <el-descriptions-item label="居住地">苏州市</el-descriptions-item>
        <el-descriptions-item label="备注">
          <el-tag size="small">学校</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="联系地址">江苏省苏州市吴中区吴中大道 1188 号</el-descriptions-item>
      </el-descriptions>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogUserVisible = false">确认</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'
import { getItemListForSearch } from '@/api/items'
import { createOrder, deleteOrder, getOrderList, updateOrder } from '@/api/orders'
import { getInfo, getUserListForSearch } from '@/api/user' // secondary package based on el-pagination

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      userOrderList: null,
      total: 0,
      listLoading: true,
      activeName: 'first',
      rejectReason: null,
      listQuery: {
        page: 1,
        limit: 10,
        item_id: [],
        desc: null,
        user_id: [],
        orderState: [],
        timeDesc: null
      },
      item_list: [],
      user_list: [],
      sortOptions: [{ label: 'ID 降序', key: true }, { label: 'ID 升序', key: false }],
      orderStatusOption: [{ label: '待处理', key: 0 }, { label: '正在处理', key: 1 },
        { label: '被拒绝', key: 2 }, { label: '完成交易', key: 3 }, { label: '交易失败', key: 4 }],
      showReviewer: false,
      addOrderForm: {
        name: '',
        create_time: new Date(),
        description: '',
        user_id: this.$store.getters.userInfo.id,
        item_id: null
      },
      dialogRejectVisible: false,
      dialogFormVisible: false,
      dialogUserVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑订单窗口',
        create: '创建订单窗口'
      },
      total_num_items: 0,
      userData: [],
      rules: {
        name: [{ required: true, message: '请输入标题', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getQueryList()
    this.getOrderList()
  },
  methods: {
    parseTime(value) {
      return parseTime(Date.parse(value), '{y}-{m}-{d} {h}:{i}')
    },
    getOrderId(index) {
      let id = index + 1 + (this.listQuery.page - 1) * this.listQuery.limit
      if (this.listQuery.desc) {
        id = this.total - id + 1
      }
      return id
    },
    processStatus(status) {
      const result = []
      switch (status) {
        case 0:
          result.push('info')
          result.push('尚未处理')
          result.push(false)
          break
        case 1:
          result.push('primary')
          result.push('订单处理中')
          break
        case 2:
          result.push('danger')
          result.push('订单被拒绝')
          break
        case 3:
          result.push('success')
          result.push('订单完成')
          break
        case 4:
          result.push('danger')
          result.push('交易失败')
          break
        default:
          break
      }
      return result
    },
    // 获得用户信息的函数未定义

    async handlegetUserData(user_id) {
      this.dialogUserVisible = true
      const { data: res } = await getInfo(user_id)
      this.userData = res
    },

    // 后台接受订单
    async handleAccept(row) {
      const update_data = {
        id: row.id
      }
      update_data.status = 1
      await updateOrder(update_data)
      this.getOrderList
    },
    // 后台拒绝订单
    async handleReject(row) {
      const update_data = {
        id: row.id
      }
      update_data.status = 2
      update_data.reject_or_fail_reason = this.rejectReason
      await updateOrder(update_data)
      this.getOrderList
    },

    async getQueryList() {
      const { data: res } = await getItemListForSearch()
      this.item_list = res.goodslist
      this.total_num_items = res.total
      const { data: user_res } = await getUserListForSearch()
      this.user_list = user_res
    },
    async getOrderList() {
      this.listLoading = true
      const { data: res } = await getOrderList(this.listQuery)
      this.userOrderList = res.orderlist
      this.total = res.total
      // Just to simulate the time of the request
      this.listLoading = false
    },
    handleFilter() {
      // this.listQuery.page = 1
      this.getOrderList()
    },
    async handleModifyStatus(row, source) {
      const update_data = {
        id: row.id
      }
      switch (source) {
        case '发布':
          update_data.isEditing = false
          break
        case '撤回':
          update_data.isEditing = true
          break
        default:
          break
      }
      await updateOrder(update_data)
      this.getOrderList()
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      } else if (prop === 'time') {
        this.sortByTime(order)
      }
      this.handleFilter()
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.desc = false
      } else if (order === 'descending') {
        this.listQuery.desc = true
      } else {
        this.listQuery.desc = null
      }
    },
    sortByTime(order) {
      if (order === 'ascending') {
        this.listQuery.timeDesc = false
      } else if (order === 'descending') {
        this.listQuery.timeDesc = true
      } else {
        this.listQuery.timeDesc = null
      }
    },
    resetAddFormData() {
      this.addOrderForm = {
        name: '',
        create_time: new Date(),
        description: '',
        user_id: this.$store.getters.userInfo.id,
        item_id: null
      }
    },
    handleCreate() {
      this.resetAddFormData()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.addOrderForm.create_time = new Date()
          createOrder(this.addOrderForm).then(async() => {
            this.dialogFormVisible = false
            this.$notify({
              title: '成功啦',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
            await this.getOrderList()
          }).catch(() => {
            this.$message.error('创建订单失败了！')
          })
        }
      })
    },
    handleUpdate(row) {
      this.addOrderForm = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.addOrderForm)
          updateOrder(tempData).then(async() => {
            this.dialogFormVisible = false
            this.$notify({
              title: '成功啦',
              message: '编辑成功',
              type: 'success',
              duration: 2000
            })
            await this.getOrderList()
          }).catch(() => {
            this.$message.error('更新信息失败')
          })
        }
      })
    },
    async handleDelete(row) {
      await deleteOrder(row.id)
      this.$message.success('删除成功！')
      await this.getOrderList()
    }
  }
}
</script>

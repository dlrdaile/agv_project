<template>
  <div>
    <!--卡片试图区域-->
    <el-card>
      <el-row :gutter="2">
        <el-col :span="10">
          <el-select v-model="queryInfo.query" clearable @clear="getgoodsList">
            <el-option v-for="item in kindOptions" :key="item.key" :label="item.label" :value="item.key" />
          </el-select>
          <el-button
            icon="el-icon-search"
            type="primary"
            @click="getgoodsList"
          />
        </el-col>
        <el-col :offset="12" :span="2">
          <el-button type="primary" @click="goAddpage">添加零件</el-button>
        </el-col>
      </el-row>
      <!--表格区域-->
      <el-table
        :data="goodslist"
        border
        stripe
        highlight-current-row
      >
        <el-table-column type="expand">
          <template v-slot="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="零件ID:">
                <span>{{ props.row.id }}</span>
              </el-form-item>
              <el-form-item label="零件名称:">
                <span>{{ props.row.name }}</span>
              </el-form-item>
              <el-form-item label="零件价格:">
                <span>{{ props.row.price + '元' }}</span>
              </el-form-item>
              <el-form-item label="零件重量:">
                <span>{{ props.row.weight + '千克' }}</span>
              </el-form-item>
              <!-- // 是否为第三方零件 -->
              <el-form-item label="零件类型">
                <span>{{ props.row.kind }}</span>
              </el-form-item>
              <el-form-item label="创建者:">
                <span>{{ props.row.Provider }}</span>
              </el-form-item>
              <!--              <el-form-item label="所需工序">-->
              <!--                <span>{{ props.row.goods_processes }}</span>-->
              <!--              </el-form-item>-->
              <el-form-item label="商品描述">
                <span>{{ props.row.description }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          label="零件ID"
          prop="id"
        />
        <el-table-column
          label="零件名称"
          prop="name"
        />
        <el-table-column
          label="零件价格(元)"
          prop="price"
        />
        <el-table-column
          label="零件类型"
          prop="kind"
        />
        <el-table-column
          label="创建者"
          prop="Provider"
        />
        <!-- 新增工序流程一栏 -->
        <el-table-column label="工序流程" width="80px" align="center">
          <template v-slot="scope">
            <el-button type="primary" size="mini" @click="showProcess(scope.row.id)">查看</el-button>
          </template>
        </el-table-column>

        <el-table-column label="操作" min-width="120px">
          <template v-slot="scope">
            <!--            <el-button type="primary" size="mini" @click="dialogPsVisible = true">查看</el-button>-->
            <el-button type="primary" icon="el-icon-edit" size="mini" :disabled="scope.row.isCanEdit" />
            <el-button
              type="danger"
              icon="el-icon-delete"
              size="mini"
              :disabled="scope.row.isCanDelete"
              @click="removeById(scope.row.id)"
            />
            <el-button type="primary" icon="el-icon-picture" size="mini" @click="showImage(scope.row.image_path)">图片预览
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <!--分页区-->
      <el-pagination
        :current-page="queryInfo.pagenum"
        :page-sizes="[5, 10, 15, 20]"
        :page-size="queryInfo.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>
    <el-dialog :visible.sync="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog>

    <!-- 工序展示用el-descriptions组件，要求element@2.15.6以上 -->
    <el-dialog :visible.sync="dialogPsVisible" title="产品工序">
      <el-descriptions>
        <!--注意是Processes-->
        <el-descriptions-item
          v-for="(item,index) in showProcessList"
          :key="index"
          :label="'工序' + (index+1)"
        >
          {{ item }}
        </el-descriptions-item>
        <!--        <span slot="footer" class="dialog-footer">-->
        <!--          <el-button type="primary" @click="dialogPsVisible = false">确认</el-button>-->
        <!--        </span>-->
      </el-descriptions>
    </el-dialog>
  </div>
</template>
<script>
import { deleteItem, getItemList, getItemProcess } from '@/api/items'

export default {
  data() {
    return {
      // 工序对话框受显现
      dialogPsVisible: false,
      // 查询对象
      queryInfo: {
        query: '', // 查询参数
        pagenum: 1, // 当前页码
        pagesize: 10 // 每页显示条数
      },
      // 商品列表
      goodslist: [],
      // 总数据条数，用于分页
      total: 0,
      kindOptions: [
        { label: '官方商品', key: 'admin' },
        { label: '自定义商品', key: 'self' },
        { label: '第三方商品', key: 'third' }],
      dialogVisible: false,
      dialogImageUrl: '',
      showProcessList: []
    }
  },
  created() {
    this.getgoodsList()
  },
  methods: {
    showImage(img_path) {
      this.dialogImageUrl = 'https://www.dmoe.cc/random.php'
      this.dialogVisible = true
    },
    async getgoodsList() {
      const that = this
      const { data: res } = await getItemList(this.queryInfo)
      this.goodslist = res.goodslist
      this.goodslist.map(v => {
        v.isCanEdit = true
        v.isCanDelete = true
        // if (v.Provider === 'admin') {
        //   v.kind = '官方商品'
        // } else if (v.user_id === that.$store.getters.userInfo.id) {
        //   v.isCanEdit = false
        //   v.isCanDelete = false
        //   v.kind = '自定义商品'
        // } else {
        //   v.kind = '第三方商品'
        // }
        if (v.user_id === that.$store.getters.userInfo.id) {
          v.isCanEdit = false
          v.isCanDelete = false
        }
        return v
      })
      this.total = res.total
    },
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize
      this.getgoodsList()
    },
    handleCurrentChange(newPage) {
      this.queryInfo.pagenum = newPage
      this.getgoodsList()
    },
    async removeById(id) {
      const confirmResult = await this.$confirm('此操作将永久删除该零件, 是否继续?',
        '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).catch(err => {
        console.log(err)
      })

      if (confirmResult !== 'confirm') {
        return this.$message.info('已取消删除')
      }

      await deleteItem(id)
      this.$message.success('删除成功')
      await this.getgoodsList()
    },
    goAddpage() {
      this.$router.push('/goodsList/add')
    },
    async showProcess(item_id) {
      this.dialogPsVisible = true
      const { data: res } = await getItemProcess(item_id)
      this.showProcessList = res
    }
  }
}
</script>

<style lang="scss" scoped>
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
  width: 50%;
}

.filter-item {
  display: inline-block;
  vertical-align: middle;
  margin-bottom: 10px;
}
</style>

<template>
  <div>
    <!--卡片试图区域-->
    <el-card>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="queryInfo.query"
            placeholder="请输入内容"
            clearable
            @clear="getgoodsList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getgoodsList"
            />
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="goAddpage">添加零件</el-button>
        </el-col>
      </el-row>
      <!--表格区域-->
      <!-- <el-table :data="goodslist" border stripe>
        <el-table-column type="index" />
        <el-table-column label="零件名称" prop="goods_name" />
        <el-table-column label="零件价格（元）" prop="goods_price" />
        <el-table-column label="工序" prop="goods_processes" />
        <el-table-column label="创建时间" prop="add_time" />
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" icon="el-icon-edit" size="mini" />
            <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeById(scope.row.goods_id)" />
          </template>
        </el-table-column>
      </el-table> -->
      <el-table
    :data="getgoodsList"
    border
    style="width: 100%">
    <el-table-column type="expand">
      <template slot-scope="props">
        <el-form label-position="left" inline class="demo-table-expand">
          <el-form-item label="零件ID">
            <span>{{ props.row.goods_id }}</span>
          </el-form-item>
          <el-form-item label="零件名称">
            <span>{{ props.row.goods_name }}</span>
          </el-form-item>
          <el-form-item label="零件价格（元）">
            <span>{{ props.row.goods_price }}</span>
          </el-form-item>
          <!-- // 是否为第三方零件 -->
          <!-- <el-form-item label="零件类型">
            <span>{{ props.row.goods_status }}</span>
          </el-form-item> -->
          <el-form-item label="创建者">
            <span>{{ props.row.goods_creator }}</span>
          </el-form-item>
          <el-form-item label="所需工序">
            <span>{{ props.row.goods_processes }}</span>
          </el-form-item>
          <el-form-item label="商品描述">
            <span>{{ props.row.desc }}</span>
          </el-form-item>
        </el-form>
      </template>
    </el-table-column>
    <el-table-column
      label="零件ID"
      prop="goods_id">
    </el-table-column>
    <el-table-column
      label="零件名称"
      prop="goods_name">
    </el-table-column>
    <el-table-column
      label="零件价格"
      prop="goods_price">
    </el-table-column>
    <!-- <el-table-column
      label="零件类型"
      prop="goods_status">
    </el-table-column> -->
    <el-table-column
      label="创建者"
      prop="goods_creator">
    </el-table-column>
    <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" icon="el-icon-edit" size="mini" />
            <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeById(scope.row.goods_id)" />
            <el-button type="primary" icon="el-icon-picture">图片预览</el-button>
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
  </div>
</template>
<script>
import { info } from 'console'

export default {
  data() {
    return {
      // 查询对象
      queryInfo: {
        query: '', // 查询参数
        pagenum: 1, // 当前页码
        pagesize: 10 // 每页显示条数
      },
      // 商品列表
      goodslist: [],
      // 总数据条数，用于分页
      total: 0
    }
  },
  created() {
    this.getgoodsList()
  },
  methods: {
    async getgoodsList() {
      const { data: res } = this.$http.get('goods', {
        param: this.queryInfo })

      if (res.meta.status !== 200) {
        return this.$message.error('获取列表失败')
      }
      this.$message.success('获取列表成功')
      console.log(res.data)
      // 赋值
      this.goodslist = res.data.goodslist
      this.total = res.data.total
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
      const confirmResult = await this.$confirm('此操作将永久删除该零件, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).catch(err => err)

      if (confirmResult !== 'confirm') {
        return this.$message.info('已取消删除')
      }

      const { data: res } = await
      this.$http.delete('goods/${id}')

      if (res.meta.status !== 200) {
        return this.$message.error('删除失败')
      }

      this.$message.success('删除成功')
      this.getgoodsList()
    },
    goAddpage() {
      this.$router.push('/example/goodsList/add')
    }
  }
}
</script>

<style lang="less" scoped>
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
</style>

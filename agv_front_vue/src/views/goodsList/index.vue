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
      <el-table :data="goodslist" border stripe>
        <el-table-column type="index" />
        <el-table-column label="零件名称" prop="goods_name" />
        <el-table-column label="零件价格（元）" prop="goods_price" />
        <el-table-column label="工序" prop="goods_process" />
        <el-table-column label="创建时间" prop="add_time" />
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" icon="el-icon-edit" size="mini" />
            <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeById(scope.row.goods_id)" />
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
</style>

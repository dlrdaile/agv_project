<template>
  <div>
    <el-card>
      <!--提示区域-->
      <el-alert
        title="添加产品信息"
        type="info"
        center
        show-icon
        :closable="false"
      />
      <!--步骤条区-->
      <el-steps :space="200" :active="activeIndex - 0" finish-status="success" align-center>
        <el-step title="基本信息" />
        <el-step title="零件工序" />
        <el-step title="零件图片" />
        <el-step title="零件描述" />
        <el-step title="完成" />
      </el-steps>
      <!--tab栏区域-->
      <el-form ref="addFormRef" :model="addForm" :rules="addFormRules" label-width="100px">
        <el-tabs v-model="activeIndex" :tab-position="'left'" @tab-click="tabClicked">
          <el-tab-pane label="基本信息" name="0">
            <el-form-item label="零件名称" prop="goods_name">
              <el-input v-model="addForm.goods_name" style="width: 300px" />
            </el-form-item>
            <el-form-item label="零件价格" prop="goods_price">
              <el-input v-model="addForm.goods_price" type="number" style="width: 300px" />
            </el-form-item>
            <el-form-item label="零件重量" prop="goods_weight">
              <el-input v-model="addForm.goods_weight" type="number" style="width: 300px" />
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="零件工序" name="1">
            <el-alert
              title="请完成工序的添加"
              type="warning"
              left
              show-icon
              :closable="false"
            />
            <el-form-item
              v-for="(process, index) in addForm.goods_processes"
              :key="index"
              :label="'工序' + (index+1)"
              :prop="'goods_processes.' + index + '.value'"
            >
              <el-row :gutter="20">
                <el-col :span="6">
                  <!-- <el-input v-model="addForm.goods_processes.value" /> -->
                  <el-select v-model="addForm.goods_processes[index]" class="filter-item" placeholder="请选择">
                    <el-option
                      v-for="item in manyProcesses"
                      :key="item.processes_id"
                      :label="item.processes_name"
                      :value="item.processes_id"
                    />
                  </el-select>
                </el-col>
                <el-col :span="4">
                  <el-button type="danger" @click.prevent="removeProcess(process)">删除</el-button>
                </el-col>
              </el-row>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="addProcess">新增工序</el-button>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="零件图片" name="2">
            <!--action 表示图片要上传到的后台API地址（根地址加upload）-->
            <el-upload
              class="upload-demo"
              drag
              :action="baseUrl+'/client/items/add'"
              list-type="picture-card"
              :on-preview="handlePreview"
              :headers="headerObj"
              :on-success="handleSuccess"
              :auto-upload="false"
            >
              <i class="el-icon-upload" />
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            </el-upload>
          </el-tab-pane>
          <el-tab-pane label="零件描述" name="3">
            <!--富文本编辑器-->
            <quill-editor v-model="addForm.goods_introduce" />
            <!--添加商品的按钮-->
            <el-button type="primary" class="btnAdd" @click="add">添加零件</el-button>
          </el-tab-pane>
        </el-tabs>

      </el-form>
    </el-card>
    <!--图片预览-->
    <el-dialog
      title="图片预览"
      :visible.sync="previewVisible"
      width="50%"
    >
      <img :src="previewPath" alt="" width="100%">
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: '0',
      // 请求的根路径
      baseUrl: process.env.VUE_APP_BASE_API,
      // 添加表单
      addForm: {
        // 名字
        goods_name: '',
        // 价格
        goods_price: 0,
        // 重量
        goods_weight: 0,
        // 工序的数组
        goods_processes: [{ value: '' }],
        // 商品的详情描述
        goods_introduce: ''
      },
      addFormRules: {
        goods_name: [
          { required: true, message: '请输入商品名称', trigger: 'blur' }
        ],
        goods_price: [
          { required: true, message: '请输入商品价格', trigger: 'blur' }
        ],
        goods_weight: [
          { required: true, message: '请输入商品重量', trigger: 'blur' }
        ],
        goods_processes: [
          { required: true, message: '请选择产品工序', trigger: 'blur' }
        ]

      },
      // 加工工序数据  定义请求内容为processes_id和processes_name
      manyProcesses: [
        { processes_id: '1', processes_name: '工序1' },
        { processes_id: '2', processes_name: '工序2' },
        { processes_id: '3', processes_name: '工序3' }
      ],
      // 图片上传组件headers请求头对象
      headerObj: {
        Authorization: `Bearer ${this.$store.getters.token}`
      },
      // 图片的URL路径
      previewPath: '',
      previewVisible: false
    }
  },
  methods: {
    // 用于在点击标签页之后发送请求
    async tabClicked() {
      // console.log(this.activeIndex)
      if (this.activeIndex === '1') {
        const { data: res } = this.$http.get('工序所在路径')
        // 定义请求内容为processes_id和processes_name
        if (res.meta.status !== 200) {
          return this.$message.error('获取动态参数列表失败')
        }
        console.log(res.data)
        // 将接受的数据赋值到manyProcesses数组中
        this.manyProcesses = res.data
      }
    },
    removeProcess(item) {
      var index = this.addForm.goods_processes.indexOf(item)
      if (index !== -1) {
        this.addForm.goods_processes.splice(index, 1)
      }
    },
    addProcess() {
      this.addForm.goods_processes.push({
        value: '',
        key: Date.now()
      })
    },
    // 处理图片预览效果
    handlePreview(file) {
      console.log(file)
      this.previewPath = file.response.data.url
      this.previewVisible = true
    },
    // 处理移除图片的操作
    handleRemove(file) {
      // 1.获取将要删除的图片的临时路径
      const filePath = file.response.data.tmp_path
      // 2.从pics数组中找到这个图片对应的索引
      const i = this.addForm.pics.findIndex(x => x.pic === filePath)
      // 3.调用数组的splice方法，将图片信息对象从pics中移除
      this.addForm.pics.splice(i, 1)
      console.log(this.addForm)
    },
    // 监听图片上传成功的事件
    handleSuccess(response) {
      console.log(response)
      // 1.拼接得到一个图片信息对象
      const picInfo = { pic: response.data.tmp_path }
      // 2.将图片信息对象，push到pics上
      this.addForm.pics.push(picInfo)
      console.log(this.addForm)
    },
    // 添加商品
    add() {
      // console.log(this.addForm)
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) {
          return this.$message.error('请填写必要的表单项目！')
        }
        // 执行添加的业务逻辑
        const { data: res } = await this.$http.post('goods', this.addForm)

        // 成功返回的是201

        if (res.meta.status !== 201) {
          return this.$message.error('添加零件失败！')
        }

        this.$message.success('添加零件成功')
        // 跳转到商品列表
        this.$router.push('/example/goodsList')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.btnAdd {
  margin-top: 15px;
}
</style>

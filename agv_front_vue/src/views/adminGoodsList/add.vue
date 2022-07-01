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
                      :key="item.id"
                      :label="item.name"
                      :value="item.id"
                    />
                  </el-select>
                </el-col>
                <el-col :span="4">
                  <el-button type="danger" @click.prevent="removeProcess(process)">删除</el-button>
                </el-col>
              </el-row>
            </el-form-item>
            <el-col :offset="5">
              <el-button type="primary" size="medium" @click="addProcess">新增工序</el-button>
            </el-col>
          </el-tab-pane>
          <el-tab-pane label="零件图片" name="2">
            <el-upload
              ref="upload"
              class="upload-demo"
              drag
              :action="baseUrl+'/client/items/create'"
              :headers="headerObj"
              :auto-upload="false"
              :on-success="handleSuccess"
              :on-error="handleError"
              list-type="picture"
              :data="UploadGoodData"
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
            <el-row>
              <el-col :span="6">
                <el-switch
                  v-model="addForm.goods_isPublish"
                  active-text="公开"
                  inactive-text="不公开"
                />
              </el-col>
              <el-col :span="6">
                <el-button type="primary" class="btnAdd" @click="addItem">添加零件</el-button>

              </el-col>
            </el-row>

          </el-tab-pane>
        </el-tabs>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { getProcessList } from '@/api/process'

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
        goods_introduce: '',
        // 商品是否发布
        goods_isPublish: false
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
      manyProcesses: [],
      // 图片上传组件headers请求头对象
      headerObj: {
        Authorization: `Bearer ${this.$store.getters.token}`
      },
      // 图片的URL路径
      previewPath: '',
      previewVisible: false
    }
  },
  computed: {
    UploadGoodData() {
      const data = {
        name: this.addForm.goods_name,
        description: this.addForm.goods_introduce,
        isPublic: this.addForm.goods_isPublish,
        Provider: this.$store.getters.userInfo.nickname,
        price: this.addForm.goods_price,
        weight: this.addForm.goods_weight,
        Processes: this.addForm.goods_processes
      }
      return data
    }
  },
  methods: {
    // 用于在点击标签页之后发送请求
    async tabClicked() {
      if (this.activeIndex === '1') {
        const { data: res } = await getProcessList()
        this.manyProcesses = res
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
    // 监听图片上传成功的事件
    handleSuccess(response) {
      console.log(response)
      this.$message.success('零件添加成功！')
      this.$router.push('/example/goodsList')
    },
    handleError(err) {
      this.$message.error('零件添加失败！')
      console.log(err)
    },
    // 添加商品
    addItem() {
      // console.log(this.addForm)
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) {
          return this.$message.error('请填写必要的表单项目！')
        }// 跳转到商品列表
        this.$refs.upload.submit()
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

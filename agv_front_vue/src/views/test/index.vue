<template>
  <div class="test-container">
    <el-upload
      ref="upload"
      class="upload-demo"
      action="http://127.0.0.1:8000/uploadfiles/"
      drag
      list-type="picture-card"
      :on-preview="handlePictureCardPreview"
      :on-remove="handleRemove"
      :on-success="handleSucess"
      :auto-upload="false"
      multiple
      :on-error="handleError"
      :data="data"
      name="uploadFiles"
    >
      <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
      <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
    </el-upload>
    <el-dialog :visible.sync="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog>
    <el-button style="margin-left: 10px;margin-top: 20px" size="small" type="success" @click="submit">上传到服务器</el-button>
    <img src="http://127.0.0.1:8000/api/image">
  </div>
</template>

<script>
import request from '@/utils/request'

export default {
  name: 'Test',
  data() {
    return {
      dialogImageUrl: '',
      dialogVisible: false,
      data: { 'hello': 'world' }
    }
  },
  created() {
    // this.request_img()
  },
  methods: {
    request_img() {
      request.get('/image', { responseType: 'blob' }).then(res => {
        console.log('sucess')
        console.log(res)
      }).catch(err => {
        console.log(err)
      })
    },
    handleRemove(file, fileList) {
      console.log(file, fileList)
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    },
    submit() {
      this.$refs.upload.submit()
    },
    handleSucess(response, file, fileList) {
      console.log(response)
      console.log(file)
      console.log(fileList)
    },
    handleError(err, file, fileList) {
      console.log(err)
      console.log(file)
      console.log(fileList)
    }
  }
}
</script>

<style scoped>

</style>

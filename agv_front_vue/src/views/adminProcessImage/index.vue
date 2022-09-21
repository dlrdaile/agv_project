<template>
  <dv-border-box-1>
    <el-container>
      <el-header>
        <h1>图像处理</h1>
      </el-header>

      <el-main>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-select v-model="value" placeholder="工件表面检测">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-col>
        </el-row>
        <!-- <div class="mainarea"> -->
        <el-row :gutter="20">
          <el-col v-for="(item, index) in 2" :key="index" :span="12">
            <div style="margin-top: 15px">
              <el-card
                style="background: #fff;height: 450px;"
                :body-style="{ padding: '10px' }"
              >
                <div v-if="index == 0" class="word">图像处理前</div>
                <div v-else class="word">图像处理后</div>
                <img
                  v-if="index == 0"
                  :src="dialogImageUrl"
                  class="image"
                />
                <img
                  v-if="index == 1"
                  src="https://ts1.cn.mm.bing.net/th/id/R-C.deff7162fb0c016d70a41e610019b801?rik=6FZXn3hmtd7kKA&riu=http%3a%2f%2fwww.sdgssk.com%2fdata%2fupload%2f20200414%2f5e957aa38a9f3.JPG&ehk=AOMQNa9KNe9nO3nSsz97dWRmsTjVeFl0MCWHmHfWbjg%3d&risl=&pid=ImgRaw&r=0"
                  class="image"
                />
                <div style="padding: 20px" />
              </el-card>
            </div>
          </el-col>
        </el-row>
        <div>
          <el-button style="display: block; margin: 0 auto" type="primary" round
            >处理图像</el-button
          >
        </div>
          <div class="img_up" style="width: 700px; height: 600px; margin: 40px 80px;">
            <label style="color: black; font-size: 25px; font-weight: 100; margin: 10px 0px 0px 50px;">图片预览效果:</label>
            <a href="javascript:;" class="file" @click="upimgs">
              <input type="file" name="img" required>
            </a>
            <!-- 图片宽度100%，高度自适应，保持图片不变行 -->
            <div class="tableimg"><img id="img" width="100%" src="./upload.png"></div>
          </div>
        <!-- </div> -->
      </el-main>
      <el-divider direction="vertical" content-position="center" />
    </el-container>
  </dv-border-box-1>
</template>

<script>
export default {
  data() {
    return {
      dialogImageUrl: "",
      dialogVisible: false,
      disabled: false,
      currentDate: new Date(),
      options: [
        {
          value: "选项1",
          label: "黄金糕",
        },
        {
          value: "选项2",
          label: "双皮奶",
        },
        {
          value: "选项3",
          label: "蚵仔煎",
        },
        {
          value: "选项4",
          label: "龙须面",
        },
        {
          value: "选项5",
          label: "北京烤鸭",
        },
      ],
      value: "",
    };
  },
  methods: {
    handleRemove(file) {
      console.log(file);
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    handleDownload(file) {
      console.log(file);
    },
  },
};
</script>

<style>
.word {
  font-style: normal;
  font-weight: bold;
  font-size: 25px;
  text-align: center;
  font-family: "Lucida Calligraphy", cursive, serif, sans-serif;
}
.el-descriptions__body .el-descriptions__table .el-descriptions-item__cell {
  text-align: center;
}
.el-header,
.el-footer {
  background-color: rgb(189, 146, 232);
  color: #333;
  text-align: center;
  line-height: 20px;
}
.el-main {
  background-color: rgb(184, 155, 204);
  color: #333;
}
.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.el-row {
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
}

.el-card {
  min-width: 100%;
  height: 100%;
  margin-right: 20px;
  transition: all 0.5s;
}
</style>

<template>
  <el-container>
    <el-header>
      <h1>车床</h1>
    </el-header>
    <el-main>
      <!-- <div class="mainarea"> -->
      <el-row>
        <el-col v-for="o in 4" :key="o" :span="5" :offset="1">
          <div style="margin-top:15px">
            <el-card style="background: #fff" :body-style="{ padding: '10px' }">
              <img
                src="https://ts1.cn.mm.bing.net/th/id/R-C.deff7162fb0c016d70a41e610019b801?rik=6FZXn3hmtd7kKA&riu=http%3a%2f%2fwww.sdgssk.com%2fdata%2fupload%2f20200414%2f5e957aa38a9f3.JPG&ehk=AOMQNa9KNe9nO3nSsz97dWRmsTjVeFl0MCWHmHfWbjg%3d&risl=&pid=ImgRaw&r=0"
                class="image"
              >
              <div style="padding: 20px;">
                <!-- <span class="eqname">好吃的汉堡</span> -->
                <div class="bottom clearfix">
                  <!-- <time class="time">{{ currentDate }}</time>
                <el-button size="mini" type="primary" class="button">操作按钮</el-button> -->
                  <el-descriptions :column="1" border>
                    <el-descriptions-item label="序号" class="id">22</el-descriptions-item>
                    <el-descriptions-item label="描述">这是一个大机床</el-descriptions-item>
                    <el-descriptions-item label="状态">正在执行</el-descriptions-item>
                  </el-descriptions>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
      <!-- </div> -->
    </el-main>
  </el-container>

</template>

<script>
export default {
  data() {
    return {
      currentDate: new Date()
    }
  }
}
</script>

<style>
   .el-descriptions__body .el-descriptions__table .el-descriptions-item__cell {
    text-align: center;
   }
   .el-header, .el-footer {
    background-color: #468be6;
    color: #333;
    text-align: center;
    line-height: 20px;
  }
  .el-main {
    background-color: #84b5e7;
    color: #333;
  }
  .eqname {
    display:block;
    text-align:center;
  }
  .el-card {
    margin-bottom: 20px;
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
      clear: both
  }
</style>

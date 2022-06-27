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
              <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png" class="image">
              <div style="padding: 20px;">
                <span class="eqname">好吃的汉堡</span>
                <div class="bottom clearfix">
                  <!-- <time class="time">{{ currentDate }}</time>
                <el-button size="mini" type="primary" class="button">操作按钮</el-button> -->
                  <el-descriptions :column="1" border>
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

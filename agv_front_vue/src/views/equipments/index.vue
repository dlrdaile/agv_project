<template>
  <el-container>
    <el-header>
      <h1>车床</h1>
    </el-header>
    <el-main>
      <!-- <div class="mainarea"> -->
      <el-row :gutter="20">
        <el-col v-for="(item,index) in deviceList1" :key="index" :span="6">
          <div style="margin-top:15px">
            <el-card style="background: #fff" :body-style="{ padding: '10px' }">
              <img
                src="https://ts1.cn.mm.bing.net/th/id/R-C.deff7162fb0c016d70a41e610019b801?rik=6FZXn3hmtd7kKA&riu=http%3a%2f%2fwww.sdgssk.com%2fdata%2fupload%2f20200414%2f5e957aa38a9f3.JPG&ehk=AOMQNa9KNe9nO3nSsz97dWRmsTjVeFl0MCWHmHfWbjg%3d&risl=&pid=ImgRaw&r=0"
                class="image"
              >
              <div style="padding: 20px;">
                <div class="bottom clearfix">
                  <el-descriptions :column="1" border>
                    <el-descriptions-item label="序号" class="id">{{ item.id }}</el-descriptions-item>
                    <el-descriptions-item label="描述">{{ item.des }}</el-descriptions-item>
                    <el-descriptions-item label="状态">{{ item.status }}</el-descriptions-item>
                  </el-descriptions>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
      <!-- </div> -->
    </el-main>
    <el-divider direction="vertical" content-position="center" />
    <el-header>
      <h1>铣床</h1>
    </el-header>
    <el-main>
      <!-- <div class="mainarea"> -->
      <el-row :gutter="20">
        <el-col v-for="(item,index) in deviceList2" :key="index" :span="6">
          <div style="margin-top:15px">
            <el-card style="background: #fff" :body-style="{ padding: '10px' }">
              <img
                src="https://ts1.cn.mm.bing.net/th/id/R-C.c26b05d524de18c873a2d51872530dd9?rik=2%2boyNSarU%2ftsgA&riu=http%3a%2f%2fwww.luzhongmc.com%2fdata%2fupload%2f20191012%2f5da16d747c0e0.jpg&ehk=%2feXzzblnJHlnthSxb8AqWXm3qtlr7ER9o4HS%2bc6MqtA%3d&risl=&pid=ImgRaw&r=0"
                class="image"
              >
              <div style="padding: 20px;">
                <div class="bottom clearfix">
                  <el-descriptions :column="1" border>
                    <el-descriptions-item label="序号" class="id">{{ item.id }}</el-descriptions-item>
                    <el-descriptions-item label="描述">{{ item.des }}</el-descriptions-item>
                    <el-descriptions-item label="状态">{{ item.status }}</el-descriptions-item>
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
      currentDate: new Date(),
      deviceList1: [
        { id: '1',
          des: '大零件',
          status: '正在运行'
        },
        { id: '2',
          des: '小零件',
          status: '未运行'
        },
        { id: '3',
          des: '精密零件',
          status: '未运行'
        },
        { id: '4',
          des: '小零件',
          status: '正在运行'
        }

      ],
      deviceList2: [
        { id: '1',
          des: '大零件',
          status: '未运行'
        },
        { id: '2',
          des: '小零件',
          status: '正在运行'
        },
        { id: '3',
          des: '精密零件',
          status: '未运行'
        },
        { id: '4',
          des: '小零件',
          status: '正在运行'
        }

      ]
    }
  }
}
</script>

<style>
   .el-descriptions__body .el-descriptions__table .el-descriptions-item__cell {
    text-align: center;
   }
   .el-header, .el-footer {
    background-color: rgb(128, 126, 126);
    color: #333;
    text-align: center;
    line-height: 20px;
  }
  .el-main {
    background-color: #999;
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

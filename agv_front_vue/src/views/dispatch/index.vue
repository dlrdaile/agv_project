<template>
  <div>
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
      <el-tab-pane label="正在进行中" name="first"><el-container>
        <el-header>
          <h1>正在进行的订单</h1>
        </el-header>
        <el-main>
          <!-- <div class="mainarea"> -->
          <el-row :gutter="20">
            <el-col v-for="(item,index) in orderList1" :key="index" :span="6">
              <div style="margin-top:15px">
                <el-card style="background: #fff" :body-style="{ padding: '10px' }">
                  <!-- <img
                    src="https://ts1.cn.mm.bing.net/th/id/R-C.deff7162fb0c016d70a41e610019b801?rik=6FZXn3hmtd7kKA&riu=http%3a%2f%2fwww.sdgssk.com%2fdata%2fupload%2f20200414%2f5e957aa38a9f3.JPG&ehk=AOMQNa9KNe9nO3nSsz97dWRmsTjVeFl0MCWHmHfWbjg%3d&risl=&pid=ImgRaw&r=0"
                    class="image"
                  > -->
                  <div style="padding: 20px;">
                    <span class="eqname">{{ item.name }}</span>
                    <div class="bottom clearfix">
                      <el-descriptions :column="1" border>
                        <el-descriptions-item label="序号" class="id">{{ item.id }}</el-descriptions-item>
                        <el-descriptions-item label="所在机床">{{ item.status }}</el-descriptions-item>
                        <!-- <el-descriptions-item label="指导意见">{{ item.reject_or_fail_reason }}</el-descriptions-item> -->
                        <!-- <el-descriptions-item label="所有工序"><el-button type="primary">查看</el-button></el-descriptions-item> -->
                        <!-- <el-descriptions-item label="指导意见"><el-button type="primary">查看</el-button></el-descriptions-item> -->
                        <el-descriptions-item label="任务信息">
                          <el-button type="primary" @click="handlelook(item.item_id,item.reject_or_fail_reason,item.activities)">查看</el-button>
                        </el-descriptions-item>
                      </el-descriptions>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-col>
          </el-row>
          <el-pagination
            :current-page="queryInfo.pagenum"
            :page-sizes="[4, 8, 12, 16]"
            :page-size="queryInfo.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            background
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
          <!-- </div> -->
        </el-main>
      </el-container></el-tab-pane>

      <el-tab-pane label="已完成订单" name="second">
        <el-container>
          <el-header>
            <h1>已经完成的订单</h1>
          </el-header>
          <el-main>
            <!-- <div class="mainarea"> -->
            <el-row :gutter="20">
              <el-col v-for="(item,index) in orderList2" :key="index" :span="6">
                <div style="margin-top:15px">
                  <el-card style="background: #fff" :body-style="{ padding: '10px' }">
                    <!-- <img
                    src="https://ts1.cn.mm.bing.net/th/id/R-C.deff7162fb0c016d70a41e610019b801?rik=6FZXn3hmtd7kKA&riu=http%3a%2f%2fwww.sdgssk.com%2fdata%2fupload%2f20200414%2f5e957aa38a9f3.JPG&ehk=AOMQNa9KNe9nO3nSsz97dWRmsTjVeFl0MCWHmHfWbjg%3d&risl=&pid=ImgRaw&r=0"
                    class="image"
                  > -->
                    <div style="padding: 20px;">
                      <span class="eqname">{{ item.name }}</span>
                      <div class="bottom clearfix">
                        <el-descriptions :column="1" border>
                          <el-descriptions-item label="序号" class="id">{{ item.id }}</el-descriptions-item>
                          <el-descriptions-item label="所在工序">{{ item.des }}</el-descriptions-item>
                          <el-descriptions-item label="所在机床">{{ item.status }}</el-descriptions-item>
                          <el-descriptions-item label="指导意见">{{ item.status }}</el-descriptions-item>
                          <el-descriptions-item label="时间轴">
                            <el-button type="primary">查看</el-button>
                          </el-descriptions-item>
                        </el-descriptions>
                      </div>
                    </div>
                  </el-card>
                </div>
              </el-col>
            </el-row>
            <el-pagination
              :current-page="queryInfo.pagenum"
              :page-sizes="[4, 8, 12, 16]"
              :page-size="queryInfo.pageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="total"
              background
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          <!-- </div> -->
          </el-main>
        </el-container>
      </el-tab-pane>
    </el-tabs>
    <el-dialog
      title="任务信息"
      :visible.sync="dialogVisible"
    >
      <el-tabs :tab-position="tabPosition">
        <el-tab-pane label="制造工序">

          <el-descriptions>
            <!--注意是Processes-->
            <el-descriptions-item
              v-for="(item,index) in showProcessList"
              :key="index"
              :label="'工序' + (index+1)"
            >
              {{ item }}
            </el-descriptions-item>
          </el-descriptions>

          <!--制造意见-->
        </el-tab-pane>
        <el-tab-pane label="制造意见">
          <span>{{ advice }}</span>
        </el-tab-pane>

        <el-tab-pane label="完成情况">
          <el-timeline :reverse="reverse">
            <el-timeline-item
              v-for="(activity, index) in showActivities"
              :key="index"
              :timestamp="activity.timestamp"
            >
              {{ activity.content }}
            </el-timeline-item>
          </el-timeline>
        </el-tab-pane>

      </el-tabs>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
// import { getItemProcess } from '@/api/items'

import { getItemProcess } from '@/api/items'

export default {
  data() {
    return {
      queryInfo: {
        query: '', // 查询参数
        pagenum: 1, // 当前页码
        pagesize: 4 // 每页显示条数
      },
      currentDate: new Date(),
      activeName: 'first',
      total: 10,
      dialogVisible: false,
      tabPosition: 'left',
      showProcessList: [],
      advice: '暂无意见',
      showActivities: [],
      reverse: true,
      orderList1: [
        { id: '0',
          des: '大傻子',
          status: '正在进行',
          name: '订单1',
          // 制造建议用reject_or_fail_reason代替，存储在advice中
          reject_or_fail_reason: '继续加工',
          // activities的数组数据存储在showActivities中
          activities: [{
            content: '活动按期开始',
            timestamp: '2018-04-15'
          }, {
            content: '通过审核',
            timestamp: '2018-04-13'
          }, {
            content: '创建成功',
            timestamp: '2018-04-11'
          }]
        },
        { id: '2',
          des: '二傻子',
          status: '没进行',
          name: '订单2',
          reject_or_fail_reason: 'wanchengliangjian'
        },
        { id: '4',
          des: '三傻子',
          status: '正在进行',
          name: '订单3'
        },
        { id: '6',
          des: '四傻子',
          status: '正在进行',
          name: '订单4'
        },
        { id: '4',
          des: '三傻子',
          status: '正在进行',
          name: '订单5'
        }

      ],
      orderList2: [
        { id: '5',
          des: '15',
          status: 'sdf',
          name: '大会'
        },
        { id: 'sadf',
          des: 'sdf',
          status: 'gfg',
          name: '啊啊的a'
        },
        { id: 'gdfgh',
          des: 'werwer',
          status: 'ghgh',
          name: 'fs嘿嘿'
        },
        { id: '6',
          des: '四傻子',
          status: 'jhj',
          name: 'f范德萨发生da'
        },
        { id: '4',
          des: '三傻子',
          status: 'nvbn',
          name: 'fsa阿斯顿是a'
        }

      ]

    }
  },
  methods: {
    // 获取订单未完成
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize
      this.getorderList()
    },
    handleCurrentChange(newPage) {
      this.queryInfo.pagenum = newPage
      this.getorderList()
    },

    // 点击查看按钮后，传入参数（商品的ID）请求商品的所有工序
    // 同时获取指导意见（这里用reject_or_fail_reason代替）
    // 传入的三个参数分别用于在dialog中的  工序  制造意见  完成情况
    // （由于外面的card的渲染用的v-for循环,所以只能先将某一数据存储在外部，点击button传入这些参数，在dialog中渲染
    async handlelook(item_id, reject_or_fail_reason, activities) {
      this.dialogVisible = true
      this.showActivities = activities
      this.advice = reject_or_fail_reason
      const { data: res } = await getItemProcess(item_id)
      this.showProcessList = res
    }
  }
}
</script>

<style>
    /* .el-tabs__item {
			width: 250px;
			height: 47px;
			line-height: 47px;
			text-align: center;
			font-size: 20px;
			font-weight: bold
    } */
   .el-descriptions__body .el-descriptions__table .el-descriptions-item__cell {
    text-align: center;
    line-height: 20px;
    font-size: 20px;
   }
   .el-header, .el-footer {
    color: #333;
    text-align: center;
    line-height: 20px;
  }
  .el-main {
    color: #333;
  }
  .eqname {
    display:block;
    text-align:center;
		height: 47px;
		line-height: 47px;
		text-align: center;
		font-size: 30px;
		font-weight: bold
  }
  .el-row {
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap;
  }

  .el-row .el-card {
    min-width: 100%;
    margin-right: 20px;
    height: 100%;
    transition :all .5s;
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

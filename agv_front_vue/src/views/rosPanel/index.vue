<template>
  <div class="rospanel-container">
    <el-container>
      <el-header style="padding-left: 0">
        <ros-heade />
      </el-header>
      <el-main>
        <ros-main
          :ros="ros"
          :connected="connected"
        />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import RosHeade from '@/views/rosPanel/component/Header'
import RosMain from '@/views/rosPanel/component/MainBody'

export default {
  name: 'RosPanel',
  components: {
    RosHeade,
    RosMain
  },
  data() {
    return {
      connected: false,
      ros: null,
      rosNode: {},
      rosTopicInfo: {},
      rosActionInfo: {},
      rosServerInfo: {},
      rosDynamicParam: {},
      rosParam: {},
      temp: null
    }
  },
  created() {
    this.ros = new ROSLIB.Ros({
      // url: 'ws://192.168.10.47:9090'
      url: 'ws://202.81.231.27:22963'
    })
    // url: "ws://202.81.231.27:22963",
    this.ros.on('connection', () => {
      this.connected = true
      // this.getActionInfo()
      // this.getNodeInfo()
      // this.getParamInfo()
      // this.getTopicInfo()
      // this.getMessageDetails('geometry_msgs/Twist')
      // this.getServerInfo()
    })
    this.ros.on('error', () => {
      this.connected = false
      console.log('error')
    })
    this.ros.on('close', () => {
      this.connected = false
      console.log('close')
    })
  },
  methods: {
    getNodeInfo() {
      var that = this
      that.rosNode = {}
      this.ros.getNodes((result) => {
        for (const node in result) {
          const nodeName = result[node]
          that.ros.getNodeDetails(nodeName, (nodeDetail) => {
            that.rosNode[nodeName] = { ...nodeDetail }
          })
        }
      }, (error) => {
        console.log(error)
      })
    },
    getTopicInfo() {
      var that = this
      that.rosTopicInfo = {}
      this.ros.getTopics(result => {
        for (const topicIndex in result.topics) {
          const topicName = result.topics[topicIndex]
          that.rosTopicInfo[topicName] = {
            type: result.types[topicIndex]
          }
        }
      }, error => {
        console.log('getTopics error,because', error)
      })
    },
    getTopicType(topicName) {
      this.ros.getTopicType(topicName, result => {
        console.log(result)
      }, error => {
        console.log('getTopicType error,because', error)
      })
    },
    getMessageDetails(topicType) {
      this.ros.getMessageDetails(topicType, (result) => {
        console.log(result)
      }, error => {
        console.log('getMessageDetails error,because', error)
      })
    },
    getActionInfo() {
      var that = this
      that.rosActionInfo = {}
      this.ros.getActionServers(result => {
        that.rosActionInfo = result
      }, error => {
        console.log('getActionServers error,because', error)
      })
    },
    getParamInfo() {
      var that = this
      that.rosParam = {}
      this.ros.getParams(result => {
        that.rosParam = result
      }, error => {
        console.log('getParams error,because', error)
      })
    },
    getServerInfo() {
      var that = this
      that.rosServerInfo = {}
      this.ros.getServices(result => {
        for (const serviceIndex in result) {
          const serviceName = result[serviceIndex]
          that.ros.getServiceType(serviceName, result => {
            that.rosServerInfo[serviceName] = {
              serviceTypeName: result
            }
          }, error => {
            console.log(error)
          })
        }
      }, error => {
        console.log('getServices error,because', error)
      })
    },
    getServiceType(serviceName) {
      this.ros.getServiceType(serviceName, result => {
        console.log(result)
      }, error => {
        console.log('getServiceType error,because', error)
      })
    },
    getServiceResponseDetails(serviceTypeName) {
      this.ros.getServiceResponseDetails(serviceTypeName, result => {
        console.log(result)
      }, error => {
        console.log('getServiceResponseDetails error,because', error)
      })
    },
    getServiceRequestDreetails(serviceTypeName) {
      this.ros.getServiceRequestDetails(serviceTypeName, result => {
        console.log(result)
      }, error => {
        console.log('getServiceRequestDetails error,because', error)
      })
    },
    setStatusLevel(level, id) {
      this.ros.setStatusLevel(level, id)
    },
    getServicesForType(serviceTypeName) {
      this.ros.getServicesForType(serviceTypeName, result => {
        console.log(result)
      }, error => {
        console.log('getServicesForType error,because', error)
      })
    },
    getTopicsForType(topicTypeName) {
      this.ros.getTopicsForType(topicTypeName, result => {
        console.log(result)
      }, error => {
        console.log('getTopicsForType error,because', error)
      })
    }
  }
}
</script>

<style scoped lang="scss">
.el-container {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: url("../../assets/images/bg.png"); //背景图
}
</style>

const state = {
  agv_set: {}
}

class agv {
  constructor(ros, is_connect) {
    this.ros = ros
    this.connected = is_connect
  }
}

const mutations = {
  ADD_AGV: (state, agv_name, agv) => {
    state.agv_set[agv_name] = agv
  }
}

const actions = {

}

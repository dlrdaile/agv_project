<template>
  <div class="test-container">
    <h1>WebSocket Chat</h1>
    <h2>Your ID: <span id="ws-id" /></h2>
    <form action="">
      <input id="messageText" v-model="value" type="text" autocomplete="off">
      <button @click.prevent="sendMessage">Send</button>
    </form>
    <ul id="messages" />
  </div>
</template>

<script>
export default {
  name: 'Test',
  data() {
    return {
      ws: null,
      value: ''
    }
  },
  mounted() {
    const token = this.$store.getters.token
    // document.querySelector('#ws-id').textContent = this.$store.getters.userInfo.name
    // this.ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`)
    this.ws = new WebSocket(`ws://localhost:8000/ws/get_process_data?token=${token}`)
    this.ws.onmessage = function(event) {
      console.log(JSON.parse(event.data))
      // var messages = document.getElementById('messages')
      // var message = document.createElement('li')
      // var content = document.createTextNode(event.data)
      // message.appendChild(content)
      // messages.appendChild(message)
    }
  },
  beforeDestroy() {
    this.ws.close(1000, 'Work complete')
  },
  methods: {
    sendMessage() {
      this.ws.send(this.value)
      this.value = ''
    }
  }
}
</script>

<style scoped>

</style>

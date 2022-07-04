<template>
  <div id="zone_joystick">
    <div
      ref="nippleRef"
      :class="className"
      style="
        display: none;
        position: absolute;
        width: 100%;
        height: 100%;
        left: 0;
        display:block;
      "
    />
  </div>
</template>

<script>
import Vue from 'vue'
import nipplejs from 'nipplejs'

export default Vue.extend({
  name: 'VueNipple',
  props: {
    className: {
      type: String,
      required: false,
      defalut: 'nipple'
    },
    color: {
      type: String,
      required: false,
      defaults: 'blue'
    },
    size: {
      type: Number,
      required: false,
      default: 100
    },
    threshold: {
      type: Number,
      required: false,
      default: 0.1
    },
    fadeTime: {
      type: Number,
      required: false,
      default: 250
    },
    multitouch: {
      type: Boolean,
      required: false,
      default: false
    },
    maxNumberOfNipples: {
      type: Number,
      required: false,
      default: 1
    },
    dataOnly: {
      type: Boolean,
      required: false,
      default: false
    },
    position: {
      type: Object,
      required: false,
      default: () => {
        return { top: 0, left: 0 }
      }
    },
    mode: {
      type: String,
      required: false,
      default: 'dynamic'
    },
    restJoystick: {
      type: Boolean,
      required: false,
      default: true
    },
    restOpacity: {
      type: Number,
      required: false,
      default: 0.5
    },
    catchDistance: {
      type: Number,
      required: false,
      default: 200
    },
    lockX: {
      type: Boolean,
      required: false,
      default: false
    },
    lockY: {
      type: Boolean,
      required: false,
      default: false
    },
    dynamicPage: {
      type: Boolean,
      required: false,
      default: true
    },
    follow: {
      type: Boolean,
      required: false,
      defalut: true
    }
  },
  data: () => ({
    manager: null,
    nippleHandle: null
  }),
  mounted() {
    var vm = this
    vm.nippleHandle = vm.$refs.nippleRef
    vm = this
    var options = {
      zone: vm.nippleHandle,
      color: vm.color,
      size: vm.size,
      threshold: vm.threshold,
      fadeTime: vm.fadeTime,
      multitouch: vm.multitouch,
      maxNumberOfNipples: vm.maxNumberOfNipples,
      dataOnly: vm.dataOnly,
      position: vm.position,
      mode: vm.mode,
      restJoystick: vm.restJoystick,
      restOpacity: vm.restOpacity,
      lockX: vm.lockX,
      lockY: vm.lockY,
      catchDistance: vm.catchDistance,
      dynamicPage: vm.dynamicPage,
      follow: vm.follow
    }
    vm.manager = nipplejs.create(options)
    console.log('mounted nipple with options: ', options, vm.manager)
    vm.manager.on('added', (event, data) => vm.$emit('added', (event, data)))
    vm.manager.on('removed', (event, data) =>
      vm.$emit('removed', (event, data))
    )
    vm.manager.on('start', (event, data) => vm.$emit('start', (event, data)))
    vm.manager.on('end', (event, data) => vm.$emit('end', (event, data)))
    vm.manager.on('move', (event, data) => vm.$emit('move', (event, data)))
    vm.manager.on('dir', (event, data) => vm.$emit('dir', (event, data)))
    vm.manager.on('dir:up', (event, data) => vm.$emit('dir:up', (event, data)))
    vm.manager.on('dir:down', (event, data) =>
      vm.$emit('dir:down', (event, data))
    )
    vm.manager.on('dir:right', (event, data) =>
      vm.$emit('dir:right', (event, data))
    )
    vm.manager.on('dir:left', (event, data) =>
      vm.$emit('dir:left', (event, data))
    )
    vm.manager.on('plain', (event, data) => vm.$emit('plain', (event, data)))
    vm.manager.on('plain:up', (event, data) =>
      vm.$emit('plain:up', (event, data))
    )
    vm.manager.on('plain:down', (event, data) =>
      vm.$emit('plain:down', (event, data))
    )
    vm.manager.on('plain:right', (event, data) =>
      vm.$emit('plain:right', (event, data))
    )
    vm.manager.on('plain:left', (event, data) =>
      vm.$emit('plain:left', (event, data))
    )
    vm.manager.on('hidden', (event, data) => vm.$emit('hidden', (event, data)))
    vm.manager.on('destroyed', (event, data) =>
      vm.$emit('destroyed', (event, data))
    )
    vm.manager.on('pressure', (event, data) =>
      vm.$emit('pressure', (event, data))
    )
  }
})
</script>

<style lang="scss">
#zone_joystick {
  position: relative;
  box-sizing: content-box;
  width: 100%;
  height: 450px;
}
</style>

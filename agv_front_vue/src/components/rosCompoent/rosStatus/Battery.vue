<template>
  <div class="electric-panel" :class="bgClass">
    <div class="panel" :style="{transform: `rotate(${rotate}deg)`}">
      <div class="remainder" :style="{width: quantity +'%'}" />
    </div>
    <div
      v-show="showText"
      :style="{marginLeft: (parseFloat(rotate)? 0 : '10') + 'px'}"
      class="text"
    >{{ quantity }}%</div>
  </div>

</template>

<script>
/**
 * 电池电量Icon
 */
export default {
  name: 'ElectricQuantity',
  props: {
    quantity: {
      type: Number,
      default: 0
    },
    showText: {
      type: Boolean,
      default: true
    },
    rotate: {
      type: String,
      default: '0'
    }
  },
  computed: {
    bgClass() {
      if (this.quantity >= 30) {
        return 'success'
      } else if (this.quantity >= 15) {
        return 'warning'
      } else if (this.quantity >= 1) {
        return 'danger'
      } else {
        return 'danger'
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@mixin panel($color) {
  .panel {
    border-color: #{$color};
    &:before {
      background: #{$color};
    }
    .remainder {
      background: #{$color};
    }
  }
  .text {
    color: #{$color};
  }
}
.electric-panel {
  display: flex;
  justify-content: center;
  align-items: center;

  .panel {
    box-sizing: border-box;
    width: 30px;
    height: 14px;
    position: relative;
    border: 2px solid #ccc;
    padding: 1px;
    border-radius: 3px;

    &::before {
      content: '';
      border-radius: 0 1px 1px 0;
      height: 6px;
      background: #ccc;
      width: 4px;
      position: absolute;
      top: 50%;
      right: -4px;
      transform: translateY(-50%);
    }

    .remainder {
      border-radius: 1px;
      position: relative;
      height: 100%;
      width: 0%;
      left: 0;
      top: 0;
      background: #fff;
    }
  }

  .text {
    text-align: left;
    width: 42px;
  }
//   &.success {
//     @include panel($color-success);
//   }

//   &.warning {
//     @include panel($color-warning);
//   }

//   &.danger {
//     @include panel($color-danger);
//   }
}
</style>


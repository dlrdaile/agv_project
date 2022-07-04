<template>
  <div class="bolt" />
</template>

<script>
export default {
  name: 'Flash'
}
</script>

<style scoped>
@keyframes lightning-anim {
  0%{
    opacity:0;
  }
  100% {
    opacity:1;
  }
  50%{
    opacity:0;
  }
  0% {
    opacity:1;
  }
}
.bolt{
  position:absolute;
  top:50%;
  left:50%;
  transform:skewX(-10deg);
  animation: lightning-anim 2s linear infinite;
}
.bolt::before{

  content:"";
  position:absolute;
  margin-top:-1em;
  margin-left:-0.5em;
  border-top:0.75em solid transparent;
  border-right:0.3em solid #ffc400;
  border-bottom:0.75em solid #ffc400;
  border-left:0.3em solid transparent;
}
.bolt::after{
  content:"";
  position:absolute;
  margin-left:-0.1em;
  border-top:0.7em solid #ffc400;
  border-right:0.3em solid transparent;
  border-bottom:0.7em solid transparent;
  border-left:0.3em solid #ffc400;
}
</style>

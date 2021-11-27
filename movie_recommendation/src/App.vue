<template>
  <div id="app">
    <transition name="fade" mode="out-in">
      <router-view/>
    </transition>
    
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-family: 'Times New Roman', Times, serif;
}
.fade-enter-active,
    .fade-leave-active {
        transition: all 0.2s ease;
    }

    .fade-enter,
    .fade-leave-active {
        opacity: 0;
}
</style>

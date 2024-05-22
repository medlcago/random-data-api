<template>
  <div class="app">
    <RouterView/>
  </div>
</template>

<script setup>
import {RouterView} from "vue-router";
</script>

<style scoped>
.app {
  background: linear-gradient(90deg, rgba(2, 0, 36, 1) 0%, rgba(70, 70, 200, 1) 35%, rgba(0, 212, 255, 1) 100%);
}
</style>
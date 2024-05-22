<script setup>
import {computed, onMounted, ref} from 'vue';
import {logoutUser} from "@/services/auth.js";
import {useTitle} from "@vueuse/core";
import {getUser} from "@/services/user.js";


const user = ref({});

const getTgUsername = computed(() => {
  if (user.value.telegram) {
    return user.value.telegram.slice(1);
  }
})

const getEmailUsername = computed(() => {
  return user.value.email.split("@")[0];
})

onMounted(async () => {
  user.value = await getUser();
  useTitle(`Профиль ${getTgUsername.value ? getTgUsername.value : getEmailUsername.value}`)
})

</script>
<template>
  <div class="flex justify-center items-center h-screen">
    <div class="bg-white shadow-md rounded-lg p-6 flex flex-col items-center">
      <div class="w-32 h-32 rounded-full overflow-hidden mb-4">
        <img src="../assets/default-avatar.png" alt="User Avatar" class="w-full h-full object-cover"/>
      </div>
      <h2 class="text-2xl font-bold mb-2">{{ user.email }}</h2>
      <p class="text-gray-500 mb-4">{{ user.telegram }}</p>
      <div class="flex space-x-4 mb-4">
        <div class="flex items-center">
          <svg class="w-5 h-5 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"
               xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
          <a :href="`mailto:${user.email}`" class="text-blue-500 hover:underline">{{ user.email }}</a>
        </div>
        <div class="flex items-center" v-if="getTgUsername">
          <svg class="w-5 h-5 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"
               xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
          </svg>
          <a :href="`https://t.me/${getTgUsername}`" target="_blank"
             class="text-blue-500 hover:underline">{{ user.telegram }}</a>
        </div>
      </div>
      <RouterLink to="logout" @click.prevent="logoutUser"
                  class="inline-block align-baseline font-bold text-lg text-red-500 hover:text-amber-950">
        Выйти
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>

</style>
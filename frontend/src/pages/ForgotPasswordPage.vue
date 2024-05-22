<script setup> import {ref} from 'vue';
import {useTitle} from "@vueuse/core";

useTitle("Восстановление пароля");

const resetForm = ref({
  email: "",
});
const resetSent = ref(false);

</script>

<template>
  <div class="flex justify-center items-center h-screen">
    <div class="w-full max-w-lg">
      <form class="select-none">
        <div class="bg-white shadow-md rounded-lg px-8 pt-6 pb-8 mb-4">
          <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2" for="email">
              Email
            </label>
            <input
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500"
                id="email"
                type="email"
                placeholder="Введите вашу почту"
                v-model.trim="resetForm.email"
            />
          </div>
          <div class="flex items-center justify-between">
            <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-[20px] focus:outline-none focus:shadow-outline"
                type="submit">
              Восстановить пароль
            </button>
            <RouterLink to="login"
                        class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800">
              Вернуться к входу
            </RouterLink>
          </div>
          <div class="mt-4" v-if="resetSent">
            <p class="text-green-500">
              Инструкция по сбросу пароля отправлена на вашу электронную почту.
            </p>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>

</style>
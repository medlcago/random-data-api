<script setup>
import {ref} from 'vue';

import {useTitle} from "@vueuse/core";


useTitle("Логин");

const loginForm = ref({
  username: "",
  password: ""
});


const login = () => {
  console.log('Username:', loginForm.value.username);
  console.log('Password:', loginForm.value.password);
};
</script>

<template>
  <div class="flex justify-center items-center h-screen">
    <div class="w-full max-w-lg">
      <form>
        <div class="bg-white shadow-md rounded-lg px-8 pt-6 pb-8 mb-4">
          <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2" for="username">
              Имя пользователя
            </label>
            <input
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500"
                id="username"
                type="text"
                placeholder="Имя пользователя"
                v-model.trim="loginForm.username"
            />
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2" for="password">
              Пароль
            </label>
            <input
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500"
                id="password"
                type="password"
                placeholder="Введите пароль"
                v-model.trim="loginForm.password"
            />
          </div>
          <div class="flex items-center justify-between">
            <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-[20px] focus:outline-none focus:shadow-outline"
                type="submit"
                @click.prevent="login"
            >
              Войти
            </button>
            <RouterLink to="registration"
                        class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800">
              Забыли пароль?
            </RouterLink>
          </div>
          <div class="flex justify-center mt-4">
            <RouterLink to="registration"
                        class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800">
              Регистрация
            </RouterLink>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>

</style>
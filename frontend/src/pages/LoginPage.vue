<script setup>
import {computed, ref} from 'vue';

import {useTitle} from "@vueuse/core";
import {loginUser} from "@/services/auth.js";
import {useRouter} from "vue-router";

const router = useRouter();


useTitle("Логин");

const loginForm = ref({
  email: "",
  password: ""
});

const loginFailed = ref(false);

const isFormValid = computed(() => {
  return loginForm.value.email && loginForm.value.password
});


const login = async () => {
  if (isFormValid.value) {
    const loginResult = await loginUser(loginForm.value.email, loginForm.value.password);
    loginFailed.value = !loginResult;
    if (loginResult) {
      await router.replace("profile");
    }
  } else {
    loginFailed.value = true;
  }
};
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
                placeholder="example@example.com"
                v-model.trim="loginForm.email"
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
            <div class="text-red-700" v-if="loginFailed">
              Неверный логин или пароль
            </div>
          </div>
          <div class="flex items-center justify-between">
            <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-[20px] focus:outline-none focus:shadow-outline"
                type="submit"
                @click.prevent="login"
            >
              Войти
            </button>
            <RouterLink to="forgot-password"
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
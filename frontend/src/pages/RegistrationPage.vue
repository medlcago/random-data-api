<script setup>
import {computed, ref, watch} from 'vue';
import {useTitle} from "@vueuse/core";
import {registerUser} from "@/services/user.js";
import {useRouter} from "vue-router";

const router = useRouter();

useTitle("Регистрация");

const registrationForm = ref({
  email: "",
  telegram: "",
  password: "",
  confirmPassword: ""
})

const passwordMatched = ref(true);
const passwordVisible = ref(false);
const emailAlreadyExists = ref(false);

const togglePasswordVisibility = () => passwordVisible.value = !passwordVisible.value

watch(() => [registrationForm.value.password, registrationForm.value.confirmPassword], ([newPassword, newConfirmPassword]) => {
  passwordMatched.value = newPassword === newConfirmPassword;
})

const isFormValid = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const telegramRegex = /^@[a-zA-Z][\w]{4,31}$/;
  return emailRegex.test(registrationForm.value.email) &&
      (!registrationForm.value.telegram || telegramRegex.test(registrationForm.value.telegram)) &&
      registrationForm.value.password.length >= 6 &&
      passwordMatched.value;
});

const register = async () => {
  const response = await registerUser(registrationForm.value.email, registrationForm.value.telegram, registrationForm.value.password);
  if (response) {
    await router.replace("profile");
  } else {
    emailAlreadyExists.value = true;
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
              Email<span class="text-red-500 ml-1">*</span>
            </label>
            <input
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500 focus:shadow-outline"
                id="email"
                type="email"
                placeholder="example@example.com"
                v-model.trim="registrationForm.email"
                maxlength="32"
            />
            <div class="text-red-700" v-if="emailAlreadyExists">Почта уже используется</div>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2" for="telegram">
              Telegram
            </label>
            <input
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500 focus:shadow-outline"
                id="telegram"
                type="text"
                placeholder="@example"
                v-model.trim="registrationForm.telegram"
                maxlength="33"
            />
          </div>
          <div class="mb-4 relative">
            <label class="block text-gray-700 font-bold mb-2" for="password">
              Пароль<span class="text-red-500 ml-1">*</span>
            </label>
            <div class="relative">
              <input
                  class="pr-10 shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500 focus:shadow-outline"
                  id="password"
                  :type="passwordVisible ? 'text' : 'password'"
                  placeholder="Введите пароль"
                  v-model.trim="registrationForm.password"
                  :class="{'border-red-500 focus:border-red-500': !passwordMatched}"
                  maxlength="32"
              />
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer">
                <svg
                    v-if="!passwordVisible"
                    class="h-6 w-6 text-gray-400 hover:text-gray-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    @click="togglePasswordVisibility"
                >
                  <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg
                    v-else
                    class="h-6 w-6 text-gray-400 hover:text-gray-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    @click="togglePasswordVisibility"
                >
                  <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2" for="confirmPassword">
              Подтвердите пароль<span class="text-red-500 ml-1">*</span>
            </label>
            <input
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500 focus:shadow-outline"
                id="confirmPassword"
                :type="passwordVisible ? 'text' : 'password'"
                placeholder="Подтвердите пароль"
                v-model.trim="registrationForm.confirmPassword"
                :class="{'border-red-500 focus:border-red-500': !passwordMatched}"
                maxlength="32"
            />
            <div class="text-red-700" v-if="!passwordMatched">Пароли не совпадают</div>
          </div>
          <div class="flex items-center justify-between">
            <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-[20px] focus:outline-none focus:shadow-outline disabled:opacity-50 disabled:cursor-not-allowed"
                type="submit"
                @click.prevent="register"
                :disabled="!isFormValid"
            >
              Зарегистрироваться
            </button>
            <RouterLink to="login"
                        class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800">
              Уже есть аккаунт?
            </RouterLink>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>

</style>
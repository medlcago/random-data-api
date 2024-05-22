<script setup>

</script>

<template>
  <div class="flex items-center justify-center h-screen">
    <div class="max-w-lg w-full space-y-8 text-center rounded-lg p-8 bg-white select-none">
      <div>
        <h2 class="text-4xl font-bold text-black">Страница не найдена</h2>
        <p class="mt-2 text-black">
          Извините, но запрошенная вами страница не существует.
        </p>
      </div>
      <div>
        <router-link
            to="/"
            class="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Вернуться на главную
        </router-link>
      </div>
    </div>
  </div>
</template>
<style scoped>

</style>
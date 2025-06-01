<template>
  <router-link h-60 f-c-c to="/">
    <icon-custom-newlogo
      text-16
      color-primary
      style="width: 10rem; height: 10rem"
    ></icon-custom-newlogo>
    <h2
      v-show="!appStore.collapsed"
      ml-2
      mr-8
      max-w-150
      flex-shrink-0
      text-20
      font-bold
      color-primary
    >
      {{ title }}
    </h2>
  </router-link>
</template>

<script setup>
import { useAppStore } from '@/store'

const title = import.meta.env.VITE_TITLE

const appStore = useAppStore()
</script>

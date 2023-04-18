<script lang="ts">
export default {
    props: {
        title: {
            type: String,
            required: true
        }
    }
}
</script>
<template>
    <h1 class=" text-center flex justify-center text-2xl font-bold text-gray-900 mb-8">{{ title }}</h1>
</template>
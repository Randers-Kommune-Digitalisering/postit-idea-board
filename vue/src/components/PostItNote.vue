<script setup>
defineProps({
    msg: {
        type: String,
        required: true
    },
    color: {
        type: String
    }
})
</script>

<template>
    <div :style="'background-color: ' + color + '!important'">{{ msg }}</div>
</template>

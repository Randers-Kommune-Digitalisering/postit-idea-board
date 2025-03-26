<script setup>
    import { defineProps } from 'vue'
    defineProps({
        isReconnecting: {
            type: Boolean,
            required: true
        }
    })
</script>

<template>
    <div class="messageBar" v-if="!isReconnecting">Websocket forbindelsen blev tabt - Klik her for at genetablere</div>
    <div class="messageBar reconnecting" v-else>Websocket forbindelsen blev tabt - Forsøger at genetablere</div>
</template>

<style scoped>
.messageBar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
    align-items: center;
    background-color: rgb(116, 0, 0);
    color: white;
    font-size: 0.8em;
    line-height: 2em;
    cursor: pointer;
}
.reconnecting {
    background-color: rgb(116, 116, 0);
}
</style>
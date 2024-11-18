<script setup>
  import { ref } from 'vue'

  import MessageBar from './components/MessageBar.vue'
  import PostItNote from './components/PostItNote.vue'

  const WS_PROXY = '/ws'
  const isConnected = ref(false)
  const isConnecting = ref(true)

  const notes = ref([])

  const fetchNotes = async () => {
    try {
      const response = await fetch('/api/get')
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      notes.value = data
    } catch (error) {
      console.error('Error fetching notes:', error)
    }
  }

  fetchNotes()

  const randomColor = () => {
    const colors = ['#a3f7d4', '#b3f0f0', '#a8d0ff', '#c1bfff', '#fff5d1', '#fcd3c8', '#ffb3b3', '#feb3d1', '#f3a07a', '#fdd7a3', '#f3a3c3', '#b3a3ff', '#4da6ff', '#80e6c4', '#80e6e6']
    return colors[Math.floor(Math.random() * colors.length)]
  }

  var socket
  openWebsocket()
  
  function openWebsocket()
  {
    socket = new WebSocket(WS_PROXY)

    socket.addEventListener('open', function (event) {
      console.log('Connected to server')
      isConnecting.value = false
      isConnected.value = true
    })

    socket.addEventListener('close', function (event) {
      isConnected.value = false
    })

    socket.addEventListener('message', function (event) {
      //console.log("New message: " + event.data)
      notes.value.push({ id: notes.value.length + 1, data: event.data })
    })

    socket.addEventListener('error', function (event){
      console.error('WebSocket error observed:', event)
      isConnecting.value = false
      isConnected.value = false
    })
  }

  function reconnect() {
    console.log('Reconnecting to server')
    isConnecting.value = true
    openWebsocket()
  }

  /*const contactServer = () => {
    console.log('Sending message to server')
    socket.send("TEST DATA")
  }*/
</script>

<template>
  <!--h1>Idéer til digital fornyelse</h1-->
  <div class="container">
    <PostItNote v-for="note in notes" :key="note.id" :msg="note.data" :color="randomColor()" />
  </div>
  <MessageBar v-if="!isConnecting && !isConnected" @click="reconnect()" />
</template>

<style>
*{
  box-sizing: border-box;
}
body {
  margin: 0;
  width: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #ececec;
}
#app {
  text-align: center;
}

.container {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  height: 100vh;
  overflow: auto;
}
.container > * {
  padding: 0.8rem;
  border-radius: 0.5rem;
  max-width: calc(25vw - 3rem);
  text-align: left;
  position: relative;
  box-shadow: 0 0px 0.5rem rgba(0, 0, 0, 0.02);
}
</style>
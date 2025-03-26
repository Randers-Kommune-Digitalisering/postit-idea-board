<script setup>
  import { ref, onMounted } from 'vue'

  import MessageBar from './components/MessageBar.vue'
  import PostItNote from './components/PostItNote.vue'

  const WS_PROXY = '/ws'
  const isConnected = ref(false)
  const isConnecting = ref(true)
  const isReconnecting = ref(false)

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

  const getColor = (id) => {
    const colors = ['#a3f7d4', '#b3f0f0', '#a8d0ff', '#c1bfff', '#fff5d1', '#fcd3c8', '#ffb3b3', '#feb3d1', '#f3a07a', '#fdd7a3', '#f3a3c3', '#b3a3ff', '#4da6ff', '#80e6c4', '#80e6e6']
    return colors[id%colors.length]
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
      if(!isReconnecting.value)
        attemptReconnect()
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

  function attemptReconnect()
  {
    isReconnecting.value = true
    let attempts = 0;
    const maxAttempts = 5;
    const interval = 3000;

    const reconnectInterval = setInterval(() => {
      if (attempts < maxAttempts && !isConnected.value) {
        reconnect();
        attempts++;
      } else {
        clearInterval(reconnectInterval);
        isReconnecting.value = false;
      }
    }, interval);
  }

  function reconnect() {
    if(isReconnecting.value || isConnected.value)
      return

    console.log('Reconnecting to server')
    isConnecting.value = true
    openWebsocket()
  }

  /*const contactServer = () => {
    console.log('Sending message to server')
    socket.send("TEST DATA")
  }*/

  function scrollContainer() {
    const container = document.querySelector('.container');
    let scrollAmount = 0;
    const scrollStep = 0.5; // Adjust this value to control the scroll speed
    let direction = 1; // 1 for forward, -1 for backward
    let isPaused = false;

    function step() {
      if (!isPaused) {
        scrollAmount += scrollStep * direction;
        container.scrollLeft = scrollAmount;
        if (scrollAmount >= container.scrollWidth - container.clientWidth || scrollAmount <= 0) {
          direction *= -1; // Reverse direction
          isPaused = true;
          setTimeout(() => {
            isPaused = false;
            requestAnimationFrame(step);
          }, 5000); // Pause for 5 seconds before reversing
          return;
        }
      }
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  onMounted(() => {
    scrollContainer();
  })
</script>

<template>
  <h1>Idéer til digital fornyelse</h1>
  <div class="container" v-if="notes.length > 0">
    <PostItNote v-for="note in notes" :key="note.id" :msg="note.data" :color="getColor(note.id)" />
  </div>
  <div v-else class="noitems"><span>Du kan blive den første til at indsende en idé :) {{ isReconnecting }}</span></div>
  <MessageBar v-if="!isConnecting && !isConnected" @click="reconnect()" :isReconnecting="isReconnecting" />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Delius&family=Playwrite+DE+Grund:wght@100..400&family=Sour+Gummy:ital,wght@0,100..900;1,100..900&display=swap');
*{
  box-sizing: border-box;
}
body {
  margin: 0;
  width: 100%;
  font-family: "Playwrite DE Grund", Helvetica, Arial, sans-serif;
  font-size: 0.9em;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #ececec;
}
#app {
  text-align: center;
}
h1 {
  font-size: 2.5em;
  margin-top: 3rem;
  color: #51677c;
  font-family: Helvetica, Arial, sans-serif;
}
.noitems {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 7.5rem);
}
.container {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  height: calc(100vh - 7.5rem);
  overflow: auto;
}
.container > * {
  padding: 0.8rem;
  border-radius: 0.5rem;
  max-width: calc(25vw - 3rem);
  text-align: left;
  position: relative;
  box-shadow: 0 0px 0.5rem rgba(0, 0, 0, 0.05);
  text-wrap: wrap;
  word-wrap: break-word;
  text-overflow: ellipsis;
}
</style>
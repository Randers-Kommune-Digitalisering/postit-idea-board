import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import serveStatic from 'serve-static'

const VUE_PORT = process.env.VUE_PORT || 3000;
const BACKEND_PORT = process.env.BACKEND_PORT || 8080;
const WS_PORT = process.env.WS_PORT || 8765;

export default defineConfig({
  server: {
    port: VUE_PORT,
    proxy: {
      '/api/': {
        target: 'http://localhost:' + BACKEND_PORT + '/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/ws': {
        target: 'ws://localhost:' + WS_PORT,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/ws/, ''),
      }
    },
    middleware: [
      serveStatic(path.resolve(__dirname, 'public'))
    ]
  },
  plugins: [
    vue(),
  ],
  define: {
    APP_VERSION: JSON.stringify(process.env.npm_package_version),
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  optimizeDeps: {
    include: ['vue', '@vitejs/plugin-vue']
  }
})
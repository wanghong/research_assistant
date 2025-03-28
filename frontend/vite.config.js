import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      // 匹配以 /api 开头的请求
      '/api': {
        target: 'http://127.0.0.1:5000', // 后端 API 的基础 URL
        changeOrigin: true, // 开启跨域代理
        rewrite: (path) => path.replace(/^\/api/, '/api'), // 重写请求路径
      }
    }
  }
})

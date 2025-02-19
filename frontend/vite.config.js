import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // if we try to go to any slash API endpoint , we want to send that request to 5001, which is our backend server
  server:{ 
    proxy:{
      '/api':{
        target: 'http://localhost:5001',
        changeOrigin: true,
        rewrite:(path)=>path.replace(/^\/api/,'') // rewrite the path , remove the /api & just send whatever comes after 
      }
    }
  }
})

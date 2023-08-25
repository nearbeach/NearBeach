/// <reference types="vitest" />
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [
        vue()
    ],
  test: {
    // ...
      include: [
          `./tests/unit/**/*.unit.js`,
          //`./src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}`
      ]
  },
})
/// <reference types="vitest" />
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [
        vue()
    ],
    test: {
        coverage: {
            enabled: true,
            provider: "v8",
            // provider: "istanbul",
            reporter: ['text','html','json']
        },
        environment: "jsdom",
        include: [
            `./tests/unit/**/*.unit.js`,
        ],
    },
})
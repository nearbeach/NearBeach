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
            exclude: [
                `./NearBeach/static/**/*`,
                // `./NearBeach/tests/**/*`,
                `./venv/**/*`,
            ],
            provider: "v8",
            // provider: "istanbul",
            reporter: ['text','html','json']
        },
        environment: "jsdom",
        exclude: [
            `./src/js/components.js`,
            `./src/js/composables/**/*`,
        ],
        include: [
            `./tests/unit/**/*.unit.js`,
        ],
        minThreads: 2,
        maxThreads: 5
    },
})
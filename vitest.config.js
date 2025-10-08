/// <reference types="vitest" />
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // Import the path module

export default defineConfig({
    plugins: [
        vue()
    ],
    resolve: {
        alias: {
            'Components': path.resolve(__dirname, 'src/js/components'),
            'Composables': path.resolve(__dirname, 'src/js/composables'),
            'Modules': path.resolve(__dirname, 'src/js/components/modules'),
        }
    },
    test: {
        coverage: {
            enabled: true,
            exclude: [
                `NearBeach/static/**/*`,
                `venv/**/*`,
                `node_modules/**/*`
            ],
            include: [
                'src/js/components/**/*.vue',
                'src/js/vuex/**/*.js'
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
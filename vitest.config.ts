import { fileURLToPath } from 'node:url'
import { mergeConfig, defineConfig, configDefaults } from 'vitest/config'
import viteConfig from './vite.config'
import { playwright } from '@vitest/browser-playwright'

export default mergeConfig(viteConfig, defineConfig({
    test: {
        browser: {
            enabled: true,
            provider: playwright(),
            instances: [
                {browser: 'chromium'},
            ],
        },
        coverage: {
            provider: 'v8',
            exclude: [
                'e2e/**',
                'src/main.ts'
            ],
        },
        environment: 'jsdom',
        exclude: [
            ...configDefaults.exclude,
            'e2e/**'
        ],
        root: fileURLToPath(
            new URL('./', import.meta.url)
        ),
    }
}),)

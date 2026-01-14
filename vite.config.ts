import {fileURLToPath, URL} from 'node:url'
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import postcssCustomMedia from 'postcss-custom-media'
import postcssNesting from 'postcss-nesting'
import postcssGlobalData from '@csstools/postcss-global-data'
import * as path from "node:path";


// https://vite.dev/config/
export default defineConfig({
    base: "/static/",
    build: {
        manifest: "manifest.json",
        outDir: path.resolve(__dirname, './NearBeach/static/NearBeach/'),
        rollupOptions: {
            input: {
                'main': path.resolve(__dirname, './src/main.ts'),
                'style': path.resolve(__dirname, './src/styles/style.css')
                // 'style': path.resolve(__dirname, './src/style/style.css'),
            },
            output: {
                // Output JS bundles to js/ directory with -bundle suffix
                entryFileNames: `js/[name]-bundle.js`,
                assetFileNames: `css/[name].css`,
            },
        },
    },
    css: {
        postcss: {
            plugins: [
                postcssNesting,
                postcssGlobalData({
                    files: [
                        './src/styles/variables/_media_variables.css',
                    ]
                }),
                postcssCustomMedia,
            ]
        }
    },
    plugins: [
        vue(),
        vueDevTools(),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
            '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
            '@locals': fileURLToPath(new URL('./src/locals', import.meta.url)),
            '@router': fileURLToPath(new URL('./src/router', import.meta.url)),
        },
    },
})

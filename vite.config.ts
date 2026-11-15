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
        outDir: path.resolve(import.meta.dirname, './NearBeach/static/NearBeach/'),
        rolldownOptions: {
            input: {
                'main': path.resolve(import.meta.dirname, './src/main.ts'),
                'login': path.resolve(import.meta.dirname, './src/login.ts'),
                'login_style': path.resolve(import.meta.dirname, './src/styles/login_style.css'),
                'style': path.resolve(import.meta.dirname, './src/styles/style.css'),
                // Referenced only from Django templates (favicon), so it needs to be an entry
                'favicon': path.resolve(import.meta.dirname, './src/assets/NearBeach_Small.png'),
            },
            output: {
                // Output JS bundles to js/ directory with -bundle suffix
                entryFileNames: 'js/[name]-bundle.js',
                // Only stylesheets go to css/. Fonts, images etc. keep their real
                // extension, otherwise they get emitted as e.g. Roboto-Thin.css.
                assetFileNames: (assetInfo) => {
                    const name = assetInfo.names?.[0] ?? assetInfo.name ?? ''
                    if (name.endsWith('.css')) return 'css/[name].css'
                    if (/\.(woff2?|ttf|otf|eot)$/i.test(name)) return 'fonts/[name]-[hash][extname]'
                    return 'images/[name]-[hash][extname]'
                },
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
    server: {
        watch: {
            // Only the front end source needs watching. Python, docs and coverage output
            // contain tens of thousands of files and exhaust the OS file watcher limit.
            ignored: [
                '**/venv/**',
                '**/.venv/**',
                '**/__pycache__/**',
                '**/htmlcov/**',
                '**/coverage/**',
                '**/docs/**',
                '**/NearBeach/static/NearBeach/**',
            ],
        },
    },
    plugins: [
        vue(),
        // Devtools hooks into the same API Vue Test Utils uses to record emitted events
        ...(process.env.VITEST ? [] : [vueDevTools()]),
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

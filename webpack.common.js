const path = require('path');
const webpack = require('webpack');
const { VueLoaderPlugin } = require('vue-loader')
const MiniCssExtractplugin = require('mini-css-extract-plugin');
const CompressionPlugin = require('compression-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
    module: {
        rules: [{
                test: /\.s[ac]ss$/i,
                use: [{
                    loader: 'style-loader', // inject CSS to page
                }, {
                    loader: 'css-loader', // translates CSS into CommonJS modules
                }, {
                    loader: 'postcss-loader', // Run post css actions
                    options: {
                        postcssOptions: {
                            plugins: () => { // post css plugins, can be exported to postcss.config.js
                                return [
                                    require('precss'),
                                    require('autoprefixer')
                                ];
                            }
                        }
                    }
                }, {
                    loader: 'sass-loader' // compiles Sass to CSS
                }]
            }, {
                test: /\.vue$/,
                loader: 'vue-loader'
            }, {
                test: /\.(?:png|jpe?g|gif)$/i,
                use: [
                    {
                        loader: 'file-loader',
                    },
                ],
            }, {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader',
                ]
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new MiniCssExtractplugin(),
        new CompressionPlugin({
            algorithm: "brotliCompress",
            exclude: [
                "tinymce",
            ]
        }),
        new CopyPlugin({
            patterns: [
                { from: './src/resources/NearBeach.png', to: '' },
                { from: './src/resources/NearBeach_Small.png', to: '' },
                { from: './src/resources/images/', to: './images' },

                //TinyMce Files
                { from: './node_modules/tinymce/', to: './tinymce/' },
            ],
        }),
        new webpack.DefinePlugin({
            __VUE_OPTIONS_API__: true,
            __VUE_PROD_DEVTOOLS__: false,
        }),
    ],
    entry: {
        'NearBeach': './src/js/app.js',
        'login': './src/js/login.js',
        'loader': './src/js/loader.js',
    },
    output: {
        path: path.resolve(__dirname, 'NearBeach/static/NearBeach'),
        filename: '[name].min.js'
    },
};

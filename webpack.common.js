const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractplugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    module: {
        rules: [{
                test: /\.(scss)$/,
                use: [{
                    loader: 'style-loader', // inject CSS to page
                }, {
                    loader: 'css-loader', // translates CSS into CommonJS modules
                }, {
                    loader: 'postcss-loader', // Run post css actions
                    options: {
                        plugins: function () { // post css plugins, can be exported to postcss.config.js
                            return [
                                require('precss'),
                                require('autoprefixer')
                            ];
                        }
                    }
                }, {
                    loader: 'sass-loader' // compiles Sass to CSS
                }]
            }, {
                test: /\.vue$/,
                loader: 'vue-loader'
            }, {
                test: /\.(png|jpe?g|gif)$/i,
                use: [
                    {
                        loader: 'file-loader',
                    },
                ],
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new MiniCssExtractplugin(),
        new CleanWebpackPlugin(),
        new CompressionPlugin(),
        new CopyPlugin({
            patterns: [
                { from: './src/resources/whiteboard/', to: './whiteboard' },
                { from: './src/resources/NearBeach.png', to: '' },
                { from: './src/resources/NearBeach_Small.png', to: '' },
                { from: './src/resources/images/', to: './images' },
                { from: './node_modules/tinymce/', to: './tinymce' },
            ],
        }),
        new HtmlWebpackPlugin({
            title: 'Production',
        }),
    ],
    entry: {
        'NearBeach': './src/js/app.js',
        'login': './src/js/login.js',
        'whiteboard': './src/js/whiteboard.js',
        'loader': './src/js/loader.js',
    },
    output: {
        path: path.resolve(__dirname, 'NearBeach/static/NearBeach'),
        filename: '[name].min.js'
    },
    externals: {
        jQuery: 'jQuery',
        foundation: 'Foundation'
    },
    optimization: {
        //runtimeChunk: 'single',
    }
};
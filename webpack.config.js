const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractplugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
    mode: 'development',
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
            ],
        }),
    ],
    entry: './src/app.js',
    output: {
        path: path.resolve(__dirname, 'NearBeach/static/NearBeach'),
        filename: 'NearBeach.min.js'
    },
    externals: {
        jQuery: 'jQuery',
        foundation: 'Foundation'
    },
    watch: true,
    optimization: {
        //runtimeChunk: 'single',
    }
};


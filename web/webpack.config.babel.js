import webpack from 'webpack'
import CopyWebpackPlugin from 'copy-webpack-plugin'
import HtmlWebpackPlugin from 'html-webpack-plugin'

let isProduction = process.env.NODE_ENV === 'production'
let devtool = 'eval'
let plugins = [
    new webpack.optimize.CommonsChunkPlugin(
        'common', 'static/common.[hash].js'
    ),
    new HtmlWebpackPlugin({
        filename: 'index.html',
        template: 'src/index.html',
        inject: true
    }),
    new CopyWebpackPlugin([{
        from: 'src/assets/favicon.ico',
        to: 'static/favicon.ico'
    }])
]
if (isProduction) {
    devtool = 'source-map'
    plugins.push(
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        }),
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify('production')
            }
        })
    )
}

export default {
    entry: {
        index: './src/index.js'
    },
    output: {
        path: './dist',
        filename: 'static/[name].[hash].js'
    },
    module: {
        loaders: [{
                test: /\.vue$/,
                loader: 'vue'
            },
            {
                test: /\.js$/,
                loader: 'babel',
                exclude: /node_modules/
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file',
                query: {
                    name: '[name].[ext]?[hash]'
                }
            }
        ]
    },
    devtool: devtool,
    plugins: plugins,
    devServer: {
        contentBase: './dist',
        historyApiFallback: false,
        port: 8000,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': '/'
                }
            }
        }
    }
}

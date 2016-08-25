import webpack from 'webpack'
import HtmlWebpackPlugin from 'html-webpack-plugin'

let isProduction = process.env.NODE_ENV === 'production'
let entry = {}
let devtool = 'eval'
let plugins = [
    new webpack.optimize.CommonsChunkPlugin('common', 'common.[hash].js'),
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
for (let name of['index' /*, 'user', 'catalog'*/ , 'article']) {
    entry[name] = './src/' + name + '.js'
    plugins.push(new HtmlWebpackPlugin({
        filename: name + '.html',
        template: 'src/app.html',
        chunks: [name, 'common']
    }))
}

export default {
    entry: entry,
    output: {
        path: './dist',
        filename: '[name].[hash].js'
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
        historyApiFallback: true,
        noInfo: true,
        devServer: {
            proxy: {
                '/api': {
                    target: 'http://127.0.0.1:5000',
                    secure: false
                }
            }
        }
    }
}

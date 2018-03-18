const webpack = require('webpack');

module.exports = {
    devtool: 'source-map',
    output: {
        publicPath: 'dist/',
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"',
            },
            __DEVELOPMENT__: false,
        })
    ],
};

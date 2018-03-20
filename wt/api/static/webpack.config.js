const path = require('path');

module.exports = {
    entry: "./src/index",
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "bundle.js",
        publicPath: "/assets/",
        library: "wt-web-ui",
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                // issuer: { test, include, exclude },
                enforce: "pre",
                enforce: "post",
                loader: "babel-loader",
                options: {
                    presets: ["es2015"]
                }
            }
        ]
    },
    resolve: {
        modules: [
            "node_modules",
            path.resolve(__dirname, "src"),
        ],
        extensions: [".js", ".jsx"],
    },
    devtool: "source-map",
    context: __dirname,
    target: "web",
    devServer: {
        contentBase: path.join(__dirname, 'public'),
        compress: true,
        historyApiFallback: true,
        hot: true,
        noInfo: true
    }
}

const path = require('path');
const autoprefixer = require('autoprefixer');
const merge = require('webpack-merge');

const development = require('./webpack.cfg.development');
const production = require('./webpack.cfg.production');

require('babel-polyfill').default;

const TARGET = process.env.npm_lifecycle_event;

const PATHS = {
    app: path.join(__dirname, '../src'),
    build: path.join(__dirname, '../dist'),
};

process.env.BABEL_ENV = TARGET;

const common = {
    entry: [
        PATHS.app,
    ],
    output: {
        path: PATHS.build,
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['', '.jsx', '.js', '.json'],
        modulesDirectories: ['node_modules', PATHS.app],
    },
};

if (TARGET === 'start' || !TARGET) {
    module.exports = merge(development, common);
}

if (TARGET === 'build' || !TARGET) {
    module.exports = merge(production, common);
}

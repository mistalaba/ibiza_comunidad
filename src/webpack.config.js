const path = require('path');
const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');

// assets.js
const Assets = require('./assets');

module.exports = {
    entry: {
        app: "./app.js",
    },
    output: {
        path: __dirname + "/wwwroot/",
        filename: "[name].bundle.js"
    },
    plugins: [
      new CopyWebpackPlugin(
        Assets.map(asset => {
          const curr_path = `${asset}`.split(path.sep)[0];
          return {
            from: path.resolve(__dirname, `./node_modules/${asset}`),
            to: path.resolve(__dirname, `./ibiza_comunidad/static/lib/${curr_path}`)
          };
        })
      )
    ]
};

const path = require("path")
var webpack = require("webpack")

const HtmlWebpackPlugin = require("html-webpack-plugin")
const { CleanWebpackPlugin } = require("clean-webpack-plugin")
const Dotenv = require("dotenv-webpack")

const SERVER_URL = "http://localhost:8000"

module.exports = {
  mode: "development",
  entry: "./src/index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "./static/bundles/"),
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env", "@babel/preset-react"],
          },
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(png|jpg|jpeg|gif|svg|woff|woff2|eot|ttf)$/,
        type: "asset/resource",
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx"], // 自動解析 .js 和 .jsx 副檔名
  },
  plugins: [
    // new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      template: "./template/index.html",
    }),
    new Dotenv(),
  ],
  devServer: {
    port: 3000,
    hot: true,
    static: path.resolve(__dirname, "static/"),
    // historyApiFallback: {
    //     index: "index.html",
    // },
    proxy: [
      {
        context: ["/api"],
        target: SERVER_URL,
        // changeOrigin: true,
      },
    ],
    historyApiFallback: true,
  },
}

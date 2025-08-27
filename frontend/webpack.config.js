const path = require("path")
const webpack = require("webpack")
const TerserPlugin = require("terser-webpack-plugin")
const HtmlWebpackPlugin = require("html-webpack-plugin")
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const Dotenv = require("dotenv-webpack")

// const { PurgeCSSPlugin } = require("purgecss-webpack-plugin")
// const { BundleAnalyzerPlugin } = require("webpack-bundle-analyzer")
// const glob = require("glob")

require("dotenv").config({ path: "./.env" })

const MODE = process.env.NODE_ENV || "production"
const SERVER_URL = process.env.SERVER_URL || "http://localhost:8000"

console.log(`%cRunning in ${MODE} mode`)
console.log(`Proxying API requests to ${SERVER_URL}`)

module.exports = {
  mode: MODE,
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "main.[contenthash].js",
    clean: true,
  },
  performance: {
    hints: false, // FIXME: 暫時關閉資源大小警告, 未來需優化
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
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
      {
        test: /\.(png|jpg|jpeg|gif|svg|woff|woff2|eot|ttf)$/,
        type: "asset/resource",
      },
    ],
  },
  resolve: {
    // Auto-resolve file extensions
    extensions: [".js", ".jsx"],
  },
  optimization: {
    minimize: MODE === "production",
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            // remove console.log in production
            drop_console: true,
          },
        },
      }),
    ],
  },
  plugins: [
    // Set environment variables
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify(MODE),
    }),
    new Dotenv({ path: "./.env" }),
    new HtmlWebpackPlugin({
      template: "./template/index.html",
      filename: "index.html",
      title: "FaceRecognition System",
      inject: true,
    }),
    new MiniCssExtractPlugin({
      filename: "[name].[contenthash].css",
    }),
    // TAG: Analyze bundle size, if needed, uncomment the following lines
    // new BundleAnalyzerPlugin({
    //   analyzerMode: "disabled",
    //   generateStatsFile: false,
    // }),
    // FIXME: Reduce bundle size
    // CSS Tree-shaking, Delete unused CSS
    // new PurgeCSSPlugin({
    //   paths: glob.sync(`${path.join(__dirname, "src")}/**/*`, { nodir: true }),
    //   safelist: [/^p-/, /^pi-/], // 保留 PrimeReact 和 PrimeIcons 的 class
    // }),
  ],
  devServer: {
    port: 3000,
    hot: true,
    static: path.resolve(__dirname, "static/"),
    proxy: [
      {
        context: ["/api"],
        target: SERVER_URL,
      },
    ],
    historyApiFallback: true,
  },
}

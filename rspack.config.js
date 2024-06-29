const rspack = require("@rspack/core");
// const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");
// const { VueLoaderPlugin } = require("vue-loader");

module.exports = {
  entry: {
    main: "./frontend/index.ts",
    // auth: "./frontend/auth.ts",
    // admin: "./frontend/admin.ts",
    // board_new: "./frontend/board_new.ts",
    // thread_list: "./frontend/thread_list.ts",
    // thread_new: "./frontend/thread_new.ts",
    // thread_view: "./frontend/thread_view.ts",
    // user_profile: "./frontend/user_profile.ts",
  },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "static"),
    library: "gur",
  },
  optimization: {
    splitChunks: {
      chunks: "all",
      name: "vendor",
    },
  },
  mode: "development",
  watchOptions: {
    ignored: /node_modules/,
  },
  plugins: [
    new rspack.DefinePlugin({
      __VUE_OPTIONS_API__: false,
      __VUE_PROD_DEVTOOLS__: false,
    }),
    // new MiniCssExtractPlugin({
    //   filename: "[name].css",
    // }),
    // new VueLoaderPlugin(),
  ],
  module: {
    rules: [
      // {
      //   test: /\.vue$/,
      //   use: "vue-loader",
      // },
      // {
      //   test: /\.ts$/,
      //   use: [
      //     {
      //       loader: "ts-loader",
      //       options: {
      //         appendTsSuffixTo: [/\.vue$/],
      //       },
      //     },
      //   ],
      //   exclude: /node_modules/,
      // },
      // {
      //   test: /\.css$/,
      //   use: [
      //     {
      //       loader: MiniCssExtractPlugin.loader,
      //       options: {},
      //     },
      //     {
      //       loader: "css-loader",
      //       options: {
      //         importLoaders: 1,
      //       },
      //     },
      //     "postcss-loader",
      //   ],
      // },
      {
        test: /\.(png|jpg|gif)$/,
          type: "asset/resource",
        // use: [
        //   {
        //     loader: "file-loader",
        //     options: {
        //       outputPath: "image",
        //       publicPath: "/static/image",
        //       name: "[name].[ext]",
        //     },
        //   },
        // ],
      },
      {
        test: /\.svg$/,
        type: "asset/resource",
        // oneOf: [
        //   {
        //     resourceQuery: /inline/,
        //     use: ["vue-loader", "vue-svg-loader"],
        //   },
        //   {
        //     loader: "file-loader",
        //     options: {
        //       outputPath: "image",
        //       publicPath: "/static/image",
        //       name: "[name].[ext]",
        //     },
        //   },
        // ],
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use: [
          {
            loader: "file-loader",
            options: {
              outputPath: "fonts",
              publicPath: "/static/fonts",
              name: "[name].[ext]",
            },
          },
        ],
      },
    ],
  },
  // resolve: {
  //   extensions: [".ts", ".wasm", ".mjs", ".js", ".json"],
  //   alias: {
  //     vue$: "vue/dist/vue.esm-bundler.js",
  //   },
  // },
};

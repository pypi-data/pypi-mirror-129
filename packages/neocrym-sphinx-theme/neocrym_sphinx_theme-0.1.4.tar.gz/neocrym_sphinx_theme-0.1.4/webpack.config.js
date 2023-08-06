const { resolve } = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

module.exports = {
  mode: "production",
  devtool: "source-map",
  entry: {
    "neocrym-sphinx-theme": [
      "./src/neocrym_sphinx_theme/assets/scripts/neocrym-sphinx-theme.js",
      "./src/neocrym_sphinx_theme/assets/styles/neocrym-sphinx-theme.sass",
    ],
    "neocrym-sphinx-theme-extensions": ["./src/neocrym_sphinx_theme/assets/styles/neocrym-sphinx-theme-extensions.sass"],
  },
  output: {
    filename: "scripts/[name].js",
    path: resolve(__dirname, "src/neocrym_sphinx_theme/theme/neocrym-sphinx-theme/static"),
  },
  plugins: [new MiniCssExtractPlugin({ filename: "styles/[name].css" })],
  optimization: { minimizer: [`...`, new CssMinimizerPlugin()] },
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          { loader: "css-loader", options: { sourceMap: true } },
          { loader: "postcss-loader", options: { sourceMap: true } },
          { loader: "sass-loader", options: { sourceMap: true } },
        ],
      },
    ],
  },
};

# Webpack

## Содержание

1. [Базовая конфигурация](#базовая-конфигурация)
2. [Loaders](#loaders)
3. [Optimization](#optimization)
4. [Dev Server](#dev-server)
5. [Environment Variables](#environment-variables)

---

## Базовая конфигурация

```js
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = (env, argv) => {
  const isProduction = argv.mode === 'production';

  return {
    entry: './src/index.tsx',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: isProduction ? '[name].[contenthash].js' : '[name].js',
      clean: true,
      publicPath: '/',
    },
    resolve: {
      extensions: ['.tsx', '.ts', '.js', '.jsx'],
      alias: {
        '@': path.resolve(__dirname, 'src'),
        '@components': path.resolve(__dirname, 'src/components'),
        '@hooks': path.resolve(__dirname, 'src/hooks'),
      },
    },
    module: {
      rules: [
        // TypeScript
        {
          test: /\.tsx?$/,
          use: 'ts-loader',
          exclude: /node_modules/,
        },
        // CSS
        {
          test: /\.css$/,
          use: [
            isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
            'css-loader',
          ],
        },
        // Assets
        {
          test: /\.(png|svg|jpg|jpeg|gif)$/i,
          type: 'asset/resource',
        },
      ],
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: './public/index.html',
      }),
      isProduction && new MiniCssExtractPlugin({
        filename: '[name].[contenthash].css',
      }),
    ].filter(Boolean),
    devServer: {
      static: './dist',
      hot: true,
      historyApiFallback: true,
      port: 3000,
    },
  };
};
```

## Loaders

```js
// Babel loader
{
  test: /\.(js|jsx|ts|tsx)$/,
  exclude: /node_modules/,
  use: {
    loader: 'babel-loader',
    options: {
      presets: [
        '@babel/preset-env',
        ['@babel/preset-react', { runtime: 'automatic' }],
        '@babel/preset-typescript',
      ],
    },
  },
}

// CSS Modules
{
  test: /\.module\.css$/,
  use: [
    'style-loader',
    {
      loader: 'css-loader',
      options: {
        modules: {
          localIdentName: '[name]__[local]--[hash:base64:5]',
        },
      },
    },
  ],
}

// SASS
{
  test: /\.s[ac]ss$/i,
  use: [
    'style-loader',
    'css-loader',
    'sass-loader',
  ],
}

// SVG as React Component
{
  test: /\.svg$/,
  use: ['@svgr/webpack'],
}
```

## Optimization

```js
const TerserPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true,
          },
        },
      }),
      new CssMinimizerPlugin(),
    ],
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
        common: {
          minChunks: 2,
          chunks: 'all',
          enforce: true,
        },
      },
    },
    runtimeChunk: 'single',
  },
};
```

## Code Splitting

```js
// Dynamic imports
const Dashboard = lazy(() => import(/* webpackChunkName: "dashboard" */ './pages/Dashboard'));
const Profile = lazy(() => import(/* webpackChunkName: "profile" */ './pages/Profile'));

// Prefetch
const AdminPanel = lazy(() => import(
  /* webpackChunkName: "admin" */
  /* webpackPrefetch: true */
  './pages/Admin'
));

// Preload critical chunks
import(/* webpackPreload: true */ './CriticalComponent');
```

## Dev Server

```js
module.exports = {
  devServer: {
    static: {
      directory: path.join(__dirname, 'public'),
    },
    compress: true,
    port: 3000,
    hot: true,
    open: true,
    historyApiFallback: true,
    proxy: {
      '/api': {
        target: 'http://localhost:4000',
        changeOrigin: true,
      },
    },
  },
};
```

## Environment Variables

```js
// webpack.config.js
const webpack = require('webpack');
const dotenv = require('dotenv');

module.exports = (env) => {
  const envFile = env.production ? '.env.production' : '.env.development';
  const envVars = dotenv.config({ path: envFile }).parsed || {};

  return {
    plugins: [
      new webpack.DefinePlugin({
        'process.env': JSON.stringify(envVars),
      }),
    ],
  };
};

// Использование
const apiUrl = process.env.REACT_APP_API_URL;
```

## Best Practices

```js
// Separate configs
// webpack.common.js
// webpack.dev.js
// webpack.prod.js

const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'production',
  // production specific config
});

// Bundle Analyzer
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    process.env.ANALYZE && new BundleAnalyzerPlugin(),
  ].filter(Boolean),
};

// Source maps
module.exports = {
  devtool: isProduction ? 'source-map' : 'eval-cheap-module-source-map',
};
```

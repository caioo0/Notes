/*
 * @Author: caioo0 cai_oo@sina.com
 * @Date: 2023-04-23 14:03:43
 * @LastEditors: caioo0 cai_oo@sina.com
 * @LastEditTime: 2023-04-23 14:52:57
 * @FilePath: \react\webpackdemo\webpack.config.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
// webpack.config.js

const path = require("path");
module.exports = {
    // 入口文件指定
    entry: './src/index.js',
    // 输出资源配置
    output: {
        filename: 'bundle.js'
    },
    // 打包模式：develop-开发，production-生产
    mode: 'development',
     // 新增： dev-server配置
     devServer: {
        publicPath: '/dist'  //contentBase 或者publicPath 根据版本差异设置
    }
}
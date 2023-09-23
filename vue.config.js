const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  devServer: {
    port: 8082,
    host: "localhost", //
    https: false, // 协议
   
    proxy:{
      [process.env.VUE_APP_BASE_API]:{
        target:process.env.VUE_APP_SERVER_URL,
        changeOrigin:true,
        pathRewrite:{
          ['^'+process.env.VUE_APP_BASE_API]:''
        }
      }
    } 
  },


  transpileDependencies: true,
  lintOnSave:false,
  assetsDir: 'static',
  assetsPublicPath: './',

})

module.exports = {
  lintOnSave: false,
  publicPath: '/',
  devServer: {
    port: 80,
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true
      }
    }
  }
}

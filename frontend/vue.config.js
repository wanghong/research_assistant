module.exports = {
    devServer: {
        open: true,
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true,
                pathRewrite:{"^/api":"/api"}
            }
        }
    },
    lintOnSave: false
}
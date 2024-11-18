const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        port: 5000,
    },
});

// rules: {
//     "vue/multi-word-component-names": 0,
// },

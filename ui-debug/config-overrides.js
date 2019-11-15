module.exports = function (config, env) {
  return {
    ...config,
    resolve: {
      ...config.resolve,
      alias: {
        preact: "react"
      },
    }
  }
}

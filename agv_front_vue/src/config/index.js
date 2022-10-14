// config/index.js
const configObj = {
  baseUrl: process.env.VUE_APP_BASE_IP,
  basePort: process.env.port || process.env.npm_config_port || 9528
}

export default { ...configObj }

const env = process.env.VUE_APP_ENV;

let envApiUrl = '';
console.log(env, 'env')
if (env === 'production' || env === 'dev') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_PROD}`;
} else if (env === 'staging') {
  envApiUrl = `http://${process.env.VUE_APP_DOMAIN_STAG}`;
} else {
  envApiUrl = `http://${process.env.VUE_APP_DOMAIN_DEV}`;
}

export const apiUrl = envApiUrl;
export const appName = process.env.VUE_APP_NAME;

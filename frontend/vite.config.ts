import { fileURLToPath, URL } from 'node:url';
import { execSync } from 'node:child_process'; // Ensure correct import
import svgLoader from 'vite-svg-loader';

import { defineConfig, loadEnv, UserConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import VueDevTools from 'vite-plugin-vue-devtools';
import gitDescribe from 'git-describe';

// function getGitTag() {
//   const gitInfo = gitDescribe.gitDescribeSync();
//   return gitInfo.tag;
// }

function getGitTag() {
  try {
    // Check if Git is available
    execSync('git --version', { stdio: 'ignore' });
    // If Git is available, proceed to get the tag
    const gitInfo = gitDescribe.gitDescribeSync();
    return gitInfo.tag;
  } catch (error) {
    // If Git is not available, return a default value or handle the error
    console.warn('Git is not available, using default version');
    return 'v0.0.0';
  }
}

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());
  const config: UserConfig = {
    define: {
      'import.meta.env.VITE_APP_VERSION': JSON.stringify(getGitTag()),
    },
    base: '/',
    plugins: [vue(), svgLoader(), vueJsx(), VueDevTools()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    preview: {
      port: 8080,
      strictPort: true,
    },
    server: {
      port: 8080,
      strictPort: true,
      host: true,
      origin: 'http://0.0.0.0:8080',
      proxy:
        env.VITE_PROXY_ENABLED !== 'true'
          ? undefined
          : {
              '/api': {
                target: env.VITE_PROXY_JSON_RPC_SERVER_URL,
                changeOrigin: true,
              },
              '/socket.io': {
                target: env.VITE_PROXY_WS_SERVER_URL,
                ws: true,
                rewriteWsOrigin: true,
              },
            },
    },
  };

  return config;
});

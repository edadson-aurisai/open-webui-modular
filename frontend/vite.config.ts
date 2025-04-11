import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import staticCopy from 'vite-plugin-static-copy';

// /** @type {import('vite').Plugin} */
// const viteServerConfig = {
// 	name: 'log-request-middleware',
// 	configureServer(server) {
// 		server.middlewares.use((req, res, next) => {
// 			res.setHeader('Access-Control-Allow-Origin', '*');
// 			res.setHeader('Access-Control-Allow-Methods', 'GET');
// 			res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
// 			res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
// 			next();
// 		});
// 	}
// };

export default defineConfig({
	plugins: [
		sveltekit(),
		staticCopy({
			targets: [
				{
					src: 'static/pyodide/*',
					dest: 'pyodide'
				},
				{
					src: 'static/assets/*',
					dest: 'assets'
				},
				{
					src: 'static/audio/*',
					dest: 'audio'
				},
				{
					src: 'static/themes/*',
					dest: 'themes'
				}
			]
		})
	],
	define: {
		APP_VERSION: JSON.stringify(process.env.npm_package_version),
		APP_BUILD_HASH: JSON.stringify(process.env.APP_BUILD_HASH || 'dev-build')
	},
	server: {
		port: 3000,
		strictPort: false,
		host: true
	},
	build: {
		target: 'esnext',
		sourcemap: true
	},
	optimizeDeps: {
		exclude: ['@codemirror/state', '@codemirror/view']
	},
	worker: {
		format: 'es'
	}
});

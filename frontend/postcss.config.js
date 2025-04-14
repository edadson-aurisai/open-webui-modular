export default {
	plugins: {
		'@tailwindcss/postcss': {
			content: [
				'./src/**/*.{html,js,svelte,ts}',
				'./src/**/*.svelte',
				'./src/**/*.ts',
				'./src/**/*.js'
			],
			theme: {
				extend: {
					colors: {
						primary: 'var(--color-primary)',
						secondary: 'var(--color-secondary)',
						accent: 'var(--color-accent)',
						background: 'var(--color-background)',
						foreground: 'var(--color-foreground)'
					}
				}
			}
		}
	}
};

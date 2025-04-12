<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { WEBUI_NAME, showSidebar } from '$lib/stores';
	import MenuLines from '$lib/components/icons/MenuLines.svelte';
	import { page } from '$app/stores';

	const i18n = getContext('i18n');

	onMount(async () => {});
</script>

<svelte:head>
	<title>
		{$i18n.t('Playground')} | {$WEBUI_NAME}
	</title>
</svelte:head>

<div class="flex flex-col h-full">
	<nav
		class="sticky top-0 z-30 flex items-center justify-between w-full h-14 px-4 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900"
	>
		<div class="flex items-center gap-2">
			<button
				class="flex md:hidden items-center justify-center h-8 w-8 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
				on:click={() => showSidebar.set(!$showSidebar)}
				aria-label={$i18n.t('Toggle Sidebar')}
			>
				<MenuLines />
			</button>
			<div class="text-lg font-medium">{$i18n.t('Playground')}</div>

			<div class="flex gap-1 scrollbar-none overflow-x-auto w-fit text-center text-sm font-medium rounded-full bg-transparent pt-1">
				<a
					class="min-w-fit rounded-full p-1.5 {$page.url.pathname === '/playground' || $page.url.pathname === '/playground/'
						? 'bg-gray-100 dark:bg-gray-800'
						: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
					href="/playground">{$i18n.t('Chat')}</a
				>

				<a
					class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes('/playground/completions')
						? 'bg-gray-100 dark:bg-gray-800'
						: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
					href="/playground/completions">{$i18n.t('Completions')}</a
				>

				<a
					class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes('/playground/notes')
						? 'bg-gray-100 dark:bg-gray-800'
						: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
					href="/playground/notes">{$i18n.t('Notes')}</a
				>
			</div>
		</div>
	</nav>

	<div class="flex-1 max-h-full overflow-y-auto">
		<slot />
	</div>
</div>

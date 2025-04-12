<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import {
		WEBUI_NAME,
		showSidebar,
		functions,
		user,
		mobile,
		models,
		prompts,
		knowledge,
		tools
	} from '$lib/stores';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	import MenuLines from '$lib/components/icons/MenuLines.svelte';

	const i18n = getContext('i18n');

	let loaded = false;

	onMount(async () => {
		// Check permissions
		if (!$user?.permissions?.workspace) {
			await goto('/');
		}
		loaded = true;
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Workspace')} | {$WEBUI_NAME}
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
			<div class="text-lg font-medium">{$i18n.t('Workspace')}</div>

			<div class="flex gap-1 scrollbar-none overflow-x-auto w-fit text-center text-sm font-medium rounded-full bg-transparent pt-1">
				{#if $user?.permissions?.workspace?.models}
					<a
						class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes('/workspace/models')
							? 'bg-gray-100 dark:bg-gray-800'
							: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
						href="/workspace/models">{$i18n.t('Models')}</a
					>
				{/if}

				{#if $user?.permissions?.workspace?.knowledge}
					<a
						class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes('/workspace/knowledge')
							? 'bg-gray-100 dark:bg-gray-800'
							: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
						href="/workspace/knowledge">{$i18n.t('Knowledge')}</a
					>
				{/if}

				{#if $user?.permissions?.workspace?.prompts}
					<a
						class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes('/workspace/prompts')
							? 'bg-gray-100 dark:bg-gray-800'
							: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
						href="/workspace/prompts">{$i18n.t('Prompts')}</a
					>
				{/if}

				{#if $user?.permissions?.workspace?.tools}
					<a
						class="min-w-fit rounded-full p-1.5 {$page.url.pathname.includes('/workspace/tools')
							? 'bg-gray-100 dark:bg-gray-800'
							: 'text-gray-300 dark:text-gray-600 hover:text-gray-700 dark:hover:text-white'} transition"
						href="/workspace/tools">{$i18n.t('Tools')}</a
					>
				{/if}
			</div>
		</div>
	</nav>

	<div class="flex-1 max-h-full overflow-y-auto">
		{#if loaded}
			<slot />
		{/if}
	</div>
</div>

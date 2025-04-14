<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { fade } from 'svelte/transition';
	
	import {
		config,
		user,
		settings,
		showSettings
	} from '$lib/stores';

	import Sidebar from '$lib/components/layout/Sidebar.svelte';
	import SettingsModal from '$lib/components/chat/SettingsModal.svelte';

	const i18n = getContext('i18n');

	let loaded = false;

	onMount(async () => {
		if ($user === undefined || $user === null) {
			await goto('/auth');
		} else {
			// Basic initialization
			loaded = true;
		}
	});
</script>

<div class="flex h-screen overflow-hidden bg-background">
	<Sidebar />

	<div class="flex-1 overflow-auto">
		{#if loaded}
			<main class="flex-1 overflow-auto">
				<slot />
			</main>
		{/if}
	</div>

	{#if $showSettings}
		<div transition:fade={{ duration: 200 }}>
			<SettingsModal />
		</div>
	{/if}
</div> 
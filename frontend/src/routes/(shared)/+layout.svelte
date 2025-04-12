<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { WEBUI_NAME } from '$lib/stores';

	const i18n = getContext('i18n');

	onMount(async () => {});
</script>

<svelte:head>
	<title>
		{$i18n.t('Shared')} | {$WEBUI_NAME}
	</title>
</svelte:head>

<div class="flex flex-col h-full">
	<div class="flex-1 max-h-full overflow-y-auto">
		<slot />
	</div>
</div>

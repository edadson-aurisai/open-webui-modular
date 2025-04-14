<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		goto('/playground');
	});
</script>

<div>Redirecting...</div>

<script lang="ts">
	import type { LayoutProps } from './$types';
	import { backendUrlStore } from '$lib/config.svelte';

	let { children }: LayoutProps = $props();
</script>

<aside>
	<input bind:value={$backendUrlStore} placeholder="Backend URL" style="width:800px" />
</aside>
<main>
	{@render children()}
</main>

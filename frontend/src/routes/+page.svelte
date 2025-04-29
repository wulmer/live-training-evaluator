<script lang="ts">
	import { onMount } from 'svelte';
	import { backendUrlStore, timeSpanMin } from '$lib/config.svelte';

	$: currentLabels = [] as string[];

	async function updateLabels() {
		let res: Response;
		try {
			const fetchURL = new URL(`${$backendUrlStore}/results/`);
			fetchURL.searchParams.set('maxAgeMin', $timeSpanMin.toString());
			console.log('Fetching data from backend...', fetchURL.toString());
			res = await fetch(fetchURL);
		} catch (error) {
			console.error('Error fetching data:', error);
			return;
		}
		const json = await res.json();

		const labels: string[] = json.map((d) => d.label).sort((a, b) => a.localeCompare(b));
		const uniqueLabels = [...new Set(labels)];
		currentLabels = uniqueLabels;
	}

	onMount(() => {
		updateLabels();
		const timer = setInterval(() => {
			updateLabels();
		}, 2000);

		return () => {
			clearInterval(timer);
		};
	});
</script>

<section class="section">
	<h1 class="title">Available evaluations</h1>
	<p class="subtitle">Click on a label to see the evaluation.</p>
	{#if currentLabels.length === 0}
		<p>No evaluations available.</p>
	{:else}
		<div class="field is-grouped">
			{#each currentLabels as label}
				<p class="control">
					<a class="button" href={label}>{label}</a>
				</p>
			{/each}
		</div>
	{/if}
</section>

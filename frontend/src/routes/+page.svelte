<script lang="ts">
	import { onMount } from 'svelte';
	import { backendUrlStore } from '$lib/config.svelte';

	$: currentLabels = [] as string[];

	onMount(() => {
		async function updateLabels() {
			let res: Response;
			try {
				const fetchURL = new URL(`${$backendUrlStore}/results/`);
				fetchURL.searchParams.set('maxAgeMin', '300000');
				console.log('Fetching data from backend...', fetchURL.toString());
				res = await fetch(fetchURL);
			} catch (error) {
				console.error('Error fetching data:', error);
				setTimeout(updateLabels, 5000);
				return;
			}
			const json = await res.json();

			const labels: string[] = json.map((d) => d.label).sort((a, b) => a.localeCompare(b));
			const uniqueLabels = [...new Set(labels)];
			currentLabels = uniqueLabels;

			setTimeout(updateLabels, 2000);
		}

		updateLabels();
	});
</script>

<h1>Available evaluations</h1>
{#if currentLabels.length === 0}
	<p>No evaluations available.</p>
{:else}
	<p>Click on a label to see the evaluation.</p>
{/if}
<ul>
	{#each currentLabels as label}
		<li><a href={label}>{label}</a></li>
	{/each}
</ul>

<script lang="ts">
	import { onMount } from 'svelte';
	import { backendUrlStore } from '$lib/config.svelte';
	import { page } from '$app/state';

	import BarChart from '$lib/BarChart.svelte';

	type ResultData = {
		origin: string;
		label: string;
		value: number;
	};

	type GraphData = {
		label: string;
		value: number;
	};

	let data: GraphData[] = [];

	async function updateResults() {
		let res: Response;
		try {
			const fetchURL = new URL(`${$backendUrlStore}/results/`);
			fetchURL.searchParams.set('maxAgeMin', '300000');
			console.log('Fetching data from backend...', fetchURL.toString());
			res = await fetch(fetchURL);
		} catch (error) {
			console.error('Error fetching data:', error);
			setTimeout(updateResults, 5000);
			return;
		}
		const json: ResultData[] = await res.json();

		data = json
			.filter((d) => d.label === page.params.label)
			.map((d) => ({
				label: `${d.origin}`,
				value: Math.floor(d.value * 100)
			}));

		setTimeout(updateResults, 2000);
	}

	onMount(() => {
		data = [];
		updateResults();

		setTimeout(updateResults, 2000);
	});
</script>

<BarChart {data} />

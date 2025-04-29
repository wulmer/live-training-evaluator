<script lang="ts">
	import { onMount } from 'svelte';
	import { backendUrlStore, timeSpanMin } from '$lib/config.svelte';
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
			fetchURL.searchParams.set('maxAgeMin', $timeSpanMin.toString());
			fetchURL.searchParams.set('label', page.params.label);
			console.log('Fetching data from backend...', fetchURL.toString());
			res = await fetch(fetchURL);
		} catch (error) {
			console.error('Error fetching data:', error);
			return;
		}
		const json: ResultData[] = await res.json();

		data = json.map((d) => ({
			label: `${d.origin}`,
			value: Math.floor(d.value * 100)
		}));
	}

	onMount(() => {
		data = [];
		updateResults();
		const timer = setInterval(() => {
			updateResults();
		}, 1000);
		return () => {
			clearInterval(timer);
		};
	});
</script>

<section class="section">
	<h1 class="title">Evaluation: {page.params.label}</h1>
	<BarChart {data} />
</section>

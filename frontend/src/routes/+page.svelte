<script lang="ts">
import { onMount } from "svelte";
import BarChart from "$lib/BarChart.svelte";

let data = [
	{
		label: "Loading...",
		value: 0,
	},
];

onMount(() => {
	data = [];

	const interval = setInterval(async () => {
		const res = await fetch("http://127.0.0.1:8000/results/?maxAgeMin=300000");
		const json = await res.json();

		data = json.map((d) => ({
			label: `${d.origin} ${d.label}`,
			value: Math.floor(d.value * 100),
		}));
	}, 2000);

	return () => {
		clearInterval(interval);
	};
});
</script>

<BarChart {data} />
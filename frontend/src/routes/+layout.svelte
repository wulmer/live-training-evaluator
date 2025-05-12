<script lang="ts">
	import type { LayoutProps } from './$types';
	import { backendUrlStore, timeSpanMin } from '$lib/config.svelte';
	import { onMount } from 'svelte';

	let { children, data }: LayoutProps = $props();

	if (data.backendUrl && data.backendUrl !== '') {
		backendUrlStore.set(`http://${data.backendUrl}:8000`);
	}

	let currentLabels = $state([]) as string[];
	let successfulConnection = $state(false);
	let connectionStatus = $state(0);

	async function updateLabels() {
		let res: Response;
		try {
			const fetchURL = new URL(`${$backendUrlStore}/results/`);
			fetchURL.searchParams.set('maxAgeMin', $timeSpanMin.toString());
			console.log('Fetching data from backend...', fetchURL.toString());
			res = await fetch(fetchURL);
			successfulConnection = res.ok;
			connectionStatus = res.status;
		} catch (error) {
			console.error('Error fetching data:', error);
			successfulConnection = false;
			connectionStatus = 0;
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

<section class="hero is-small">
	<div class="hero-head supergraphic-container">
		<img src="Bosch-Supergraphic_RGB.svg" alt="Bosch Supergraphic" />
	</div>

	<div class="hero-body">
		<div class="level">
			<a href="/">
				<h1 class="title">Live Training Evaluation</h1>
				<h2 class="subtitle">by CR/AIE</h2>
			</a>
			<a href="/" class="button">
				<figure class="image is-24x24">
					<img src="home.svg" alt="Home" />
				</figure>
			</a>
		</div>
	</div>
</section>

{@render children()}

<section class="section">
	<h1 class="title">Available evaluations</h1>
	<p class="subtitle">Click on a label to see the evaluation.</p>
	{#if !successfulConnection}
		<div class="notification is-warning">
			<p>Could not connect to the backend. Please check your connection.</p>
			{#if connectionStatus !== 0}
				<p>Status code: {connectionStatus}</p>
			{/if}
		</div>
	{:else if currentLabels.length === 0}
		<p>No evaluations available.</p>
	{:else}
		<div class="field is-grouped">
			{#each currentLabels as label}
				<p class="control">
					<a class="button" href="/{label}">{label}</a>
				</p>
			{/each}
		</div>
	{/if}
</section>

<section class="section">
	<h1 class="title">Settings</h1>
	<p class="subtitle">Change the backend server and the time span filter.</p>
	<div class="field is-horizontal">
		<div class="field-label is-normal">
			<label class="label" for="inputUrl">Backend</label>
		</div>
		<div class="field-body">
			<div class="field is-expanded">
				<input
					class="input"
					id="inputUrl"
					bind:value={$backendUrlStore}
					type="text"
					placeholder="Please enter backend URL (http://someserver.westeurope.azurecontainer.io:8000)"
				/>
			</div>
		</div>
	</div>
	<div class="field is-horizontal">
		<div class="field-label is-normal">
			<label class="label" for="inputTimeSpan">Show only last x minutes</label>
		</div>
		<div class="field-body">
			<div class="field is-narrow">
				<input
					class="input"
					type="number"
					id="inputTimeSpan"
					bind:value={$timeSpanMin}
					placeholder="Time span filter"
				/>
			</div>
		</div>
	</div>
</section>

<style>
	.supergraphic-container {
		width: 100%;
		height: 6px;
		overflow: hidden;
	}
</style>

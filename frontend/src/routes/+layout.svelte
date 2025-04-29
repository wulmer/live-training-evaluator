<script lang="ts">
	import type { LayoutProps } from './$types';
	import { backendUrlStore, timeSpanMin } from '$lib/config.svelte';

	let { children }: LayoutProps = $props();
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

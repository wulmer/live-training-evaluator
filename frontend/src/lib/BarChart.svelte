<script lang="ts">
	import * as d3 from 'd3';
	import { flip } from 'svelte/animate';
	import { fade } from 'svelte/transition';

	type Data = {
		label: string;
		value: number;
	};

	// Receive plot data as prop.
	export let data: Data[] = [];
	export let showLabels = true;

	// The chart dimensions and margins as optional props.
	let width = 1800;
	export let height = 600;
	export let marginTop = 30;
	export let marginRight = 30;
	export let marginBottom = 90;
	export let marginLeft = 50;

	// Create the x (horizontal position) scale.
	$: xScale = d3
		.scaleBand()
		.domain(
			// Sort the data in descending value
			d3.groupSort(
				data,
				([d]) => d.label,
				(d) => d.label
			)
		)
		.range([marginLeft, width - marginRight])
		.padding(0.1);

	// Create the y (vertical position) scale.
	$: yScale = d3
		.scaleLinear()
		.domain([0, 100])
		.range([height - marginBottom, marginTop]);

	const boschColors = [
		'#007BC0', // Blue 50
		'#9E2896', // Purple 40
		'#004975', // Blue 30
		'#009B77', // Turquoise 50
		'#0A4F4B', // Turquoise 30
		'#00884A' // Green 50
	];
	const boschBlueColors = [
		'#b8d6ff', // Blue 85
		'#9dc9ff', // Blue 80
		'#7ebdff', // Blue 75
		'#56b0ff', // Blue 70
		'#00a4fd', // Blue 65
		'#0096e8', // Blue 60
		'#0088d4', // Blue 55
		'#007bc0', // Blue 50
		'#006ead', // Blue 45
		'#00629a', // Blue 40
		'#005587', // Blue 35
		'#004975', // Blue 30
		'#003e64', // Blue 25
		'#003253', // Blue 20
		'#002742' // Blue 15
	];
	function colorFromLabel(label: string) {
		const weights = [3, 1, 5, 2, 4, 6, 7, 8, 9, 10];
		const chars = label.split('').map((l, i) => l.charCodeAt(0) * weights[i % weights.length]);
		const charSum = chars.reduce((a, b) => a + b, 0);
		const color = boschBlueColors[charSum % Object.keys(boschBlueColors).length];
		return color;
	}
</script>

<svg viewBox="0 0 {width} {height}" style:display="block" bind:clientWidth={width}>
	<!--Add a rect for each bar. -->
	{#each data as d (d.label)}
		<rect
			style:transition="all 0.5s ease-out"
			transition:fade
			animate:flip
			fill={colorFromLabel(d.label)}
			x={xScale(d.label)}
			y={yScale(d.value)}
			height={yScale(0) - yScale(d.value)}
			width={xScale.bandwidth()}
		/>
	{/each}

	<!--X - Axis-->
	<g transform="translate(0,{height - marginBottom})">
		<line stroke="currentColor" x1={marginLeft - 6} x2={width} />

		{#each data as d}
			<!--X - Axis Ticks-->
			<line
				stroke="currentColor"
				x1={xScale(d.label) + xScale.bandwidth() / 2}
				x2={xScale(d.label) + xScale.bandwidth() / 2}
				y1={0}
				y2={6}
			/>
			{#if showLabels}
				<!-- X - Axis Tick Labels-->
				<text
					fill="currentColor"
					text-anchor="start"
					transform="rotate(-90, {xScale(d.label) + xScale.bandwidth() / 2}, 22)"
					x={xScale(d.label) + xScale.bandwidth() / 2}
					y={22}
				>
					{d.label}
				</text>
			{/if}
		{/each}
	</g>

	<!--Y - Axis-->
	<g transform="translate({marginLeft},0)">
		{#each yScale.ticks() as tick}
			<!--
      Y - Axis Ticks.
        Note: First tick is skipped since the x - axis already acts as a tick. 
      -->
			{#if tick !== 0}
				<line stroke="currentColor" x1={0} x2={-6} y1={yScale(tick)} y2={yScale(tick)} />
			{/if}

			<!--Y - Axis Tick Labels-->
			<text
				fill="currentColor"
				text-anchor="end"
				dominant-baseline="middle"
				x={-9}
				y={yScale(tick)}
			>
				{Math.trunc(tick)}
			</text>
		{/each}

		<!--Y - Axis Label-->
		<text fill="currentColor" text-anchor="start" x={-marginLeft} y={15}> ↑ value(%) </text>
	</g>
</svg>

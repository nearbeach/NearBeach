<template>
	<span class="icon">
		<svg xmlns="http://www.w3.org/2000/svg"
			 v-bind:width="width"
			 v-bind:height="height"
			 viewBox="0 0 32 32"
		>
			<polygon fill="currentColor" points="4 20 15 20 15 26.17 12.41 23.59 11 25 16 30 21 25 19.59 23.59 17 26.17 17 20 28 20 28 18 4 18 4 20"/>
			<polygon fill="currentColor" points="11 7 12.41 8.41 15 5.83 15 12 4 12 4 14 28 14 28 12 17 12 17 5.83 19.59 8.41 21 7 16 2 11 7"/>
			<rect id="_Transparent_Rectangle_" data-name="&lt;Transparent Rectangle&gt;" class="transparent-rectangle" width="32" height="32"/>
		</svg>
	</span>
</template>

<script>

export default {
	name: "CarbonDragVertical",
	props: {
		height: {
			type: String,
			default: "20px",
		},
		width: {
			type: String,
			default: "20px",
		},
	},
}
</script>

<style>
.transparent-rectangle {
	fill: none;
}
</style>

<!--ICON NAME: Carbon-->
<!--Developer: IBM-->
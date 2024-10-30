<template>
	<span class="icon">
		<svg xmlns="http://www.w3.org/2000/svg"
			 v-bind:width="width"
			 v-bind:height="height"
			 viewBox="0 0 32 32"
		>
			<path fill="currentColor" d="M19 14a3 3 0 1 0-3-3a3 3 0 0 0 3 3m0-4a1 1 0 1 1-1 1a1 1 0 0 1 1-1" />
			<path fill="currentColor" d="M26 4H6a2 2 0 0 0-2 2v20a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2m0 22H6v-6l5-5l5.59 5.59a2 2 0 0 0 2.82 0L21 19l5 5Zm0-4.83l-3.59-3.59a2 2 0 0 0-2.82 0L18 19.17l-5.59-5.59a2 2 0 0 0-2.82 0L6 17.17V6h20Z" />
		</svg>
	</span>
</template>

<script>

export default {
	name: "CarbonImage",
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

<!--ICON NAME: Carbon-->
<!--Developer: IBM-->
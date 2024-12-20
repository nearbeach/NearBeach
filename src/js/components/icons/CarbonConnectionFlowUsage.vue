<template>
	<span class="icon">
		<svg xmlns="http://www.w3.org/2000/svg"
			 v-bind:width="width"
			 v-bind:height="height"
			 viewBox="0 0 32 32"
		>
		  <path class="cls-2" d="m22,16l-1.4141,1.4141,4.5859,4.5859h-10.1719V5c0-1.1046-.8954-2-2-2H3v2h10v17c0,1.1046.8954,2,2,2h10.1719l-4.5859,4.5859,1.4141,1.4141,7-7-7-7Z"/>
		</svg>
	</span>
</template>

<script>

export default {
	name: "CarbonConnectionFlowUsage",
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
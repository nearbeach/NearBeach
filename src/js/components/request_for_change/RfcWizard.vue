<template>
	<div class="rfc-wizard--loading-bar"
		 v-bind:style="getStyle()"
	></div>

	<div class="rfc-wizard">
		<div v-for="(tab, index) in tabContents"
			 :key="tab"
			 class="rfc-wizard--tab"
		>
			<div v-bind:class="getClasses(index)">
				<span>{{ index + 1 }}</span>
			</div>
			<div class="rfc-wizard--tab-title">{{ tab }}</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "RfcWizard",
	components: {},
	props: {
		currentTab: {
			type: Number,
			default: 0,
		},
	},
	data: () => ({
		tabContents: [
			"Descript",
			"Detail",
			"Risk",
			"Implement",
			"Back-out",
			"Test Plan"
		],
	}),
	methods: {
		getClasses(index) {
			const classReturn = "rfc-wizard--tab-circle";

			// If index is current tab - we highlight as current
			if (parseInt(index) === this.currentTab) {
				return `${classReturn} current`;
			}

			// If index is less than current tab, then we are completed
			if (parseInt(index) < this.currentTab) {
				return `${classReturn} completed`;
			}

			return classReturn;
		},
		getStyle() {
			// Edge component will be 8.333% width
			// Any length between the circles is 16.666%
			const progressWidth = 8.333 + (16.333 * this.currentTab); // Renamed from 'a' to 'progressWidth'

			// Convert into string
			return `width: ${progressWidth}%;`;
		}
	},
}
</script>

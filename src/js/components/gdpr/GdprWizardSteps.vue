<template>
	<div class="gdpr-wizard--loading-bar"
		 v-bind:style="getStyle()"
	></div>

	<div class="gdpr-wizard">
		<div v-for="(tab, index) in tabContents"
			 :key="tab"
			 class="gdpr-wizard--tab"
		>
			<div v-bind:class="getClasses(index)">
				<span>{{ index + 1 }}</span>
			</div>
			<div class="gdpr-wizard--tab-title">{{ tab }}</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "GdprWizardSteps",
	components: {},
	props: {
		currentTab: {
			type: Number,
			default: 0,
		},
	},
	data: () => ({
		tabContents: [
			"Object",
			"Search",
			"Data Verification",
			"Confirmation",
		],
	}),
	methods: {
		getClasses(index) {
			const classReturn = "gdpr-wizard--tab-circle";

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
			const progressWidth = 12.5 + (25 * this.currentTab);

			// Convert into string
			return `width: ${progressWidth}%;`;
		},
	},
}
</script>

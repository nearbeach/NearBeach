<template>
	<div class="gantt-row"
		draggable="false"
	>
		<div class="gantt-row--information">
			<div>Information belongs here</div>
		</div>
		<div class="gantt-row--render"
			draggable="false"
		>
			<div class="gantt-row--render-bar">
				<div
					class="gantt-row--spacer"
					v-bind:style="`width: ${spacerWidth}px`"
				></div>
				<div
					class="gantt-row--bar"
					v-on:mousedown="mouseDown"
					v-bind:style="`width: ${barWidth}px`"
				></div>
			</div>
			<div class="gantt-row--cells">
				<div
					v-for="index in deltaDays"
					:key="index"
					class="gantt-row--cell"
				></div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "TestGanttRow",
	props: {
		deltaDays: {
			type: Number,
			default: 0,
		},
		endDate: {
			type: Number,
			default: 0,
		},
		index: {
			type: Number,
			default: 0,
		},
		startDate: {
			type: Number,
			default: 0,
		},
		startDateGantt: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			barWidth: 35,
			spacerWidth: 0,
		}
	},
	watch: {
		startDate() {
			this.setSpacerWidth();
		}
	},
	methods: {
		calculateBarWidth() {
			let delta = Math.round((this.endDate - this.startDate) / (1000 * 60 * 60 * 24));

			this.barWidth = delta * 35;
		},
		mouseDown(event) {
			//Send data up stream
			this.$emit("mouse_down", {
				clientIndex: this.index,
				clientXInitial: event.clientX,
				startDateInitial: this.startDate,
			});
		},
		setSpacerWidth() {
			let delta = Math.round((this.startDate - this.startDateGantt) / (1000 * 60 * 60 * 24));

			this.spacerWidth = delta * 35;
		},
	},
	mounted() {
		this.setSpacerWidth();
		this.calculateBarWidth();
	}
}
</script>

<style>

</style>
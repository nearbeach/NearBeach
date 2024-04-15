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
.gantt-row {
	display: flex;
	flex-direction: row;
	margin: 0;
	background-color: rgb(105, 50, 50);
	-webkit-user-select: none;
	user-select: none;
}

.gantt-row--information {
	min-width: 200px;
	max-width: 200px;
	background-color: rgb(66, 57, 57);
	display: flex;
  	flex-direction: column;
  	align-items: flex-start;
  	justify-content: center;
}

.gantt-row--cell {
	width: 35px;
	height: 35px;
	background-color: lightgrey;
	border: solid 1px dimgray;
}

.gantt-row--cells {
	display: flex;
	flex-direction: row;
	-webkit-user-select: none;
	user-select: none;
}

.gantt-row--bar {
	background-color: hotpink;
	min-width: 35px;
	//width: 70px;
	height: 20px;
	margin-top: 7px;
	z-index: 10;
}

.gantt-row--render-bar {
	position: absolute;
	display: flex;
	flex-direction: row;
}
</style>
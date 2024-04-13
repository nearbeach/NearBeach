<template>
	<div style="margin-top: 50px"></div>

	<!-- MONTH HEADER -->
	<div class="gantt-header">
		<div class="gantt-header--information"></div>
		<div class="gantt-row--months">
			<div
				v-for="month in this.monthArray"
				:key="month.index"
				class="gantt-row--month"
				v-bind:style="`width: ${month.width}px`"
			>
				{{month.month}} {{month.year}}
			</div>
		</div>
	</div>

	<!--	HEADER-->
	<div class="gantt-header">
		<div class="gantt-header--information"></div>
		<div class="gantt-row--dates">
			<div
				v-for="index in deltaDays"
				:key="index"
				class="gantt-row--date"
			>
				<div class="dayDate">
					{{getDayDate(index)}}
				</div>
				<div class="dayText">
					{{getDayText(index)}}
				</div>
			</div>
		</div>
	</div>

	<!--	RENDER-->
	<div class="gantt-row"
		 v-on:mouseup="mouseUp"
		 v-on:mouseleave="mouseLeave"
	     v-on:mousemove="mouseMove"
	>
		<div class="gantt-row--information">
			<div>Information belongs here</div>
		</div>
		<div class="gantt-row--render">
			<div class="gantt-row--render-bar">
				<div
					class="gantt-row--spacer"
					v-bind:style="`width: ${spacerWidth}px`"
				></div>
				<div
					class="gantt-row--bar"
					v-on:mousedown="mouseDown"
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

import {DateTime} from "luxon";

export default {
	name: "TestGanttChart",
	props: {},
	data() {
		return {
			clientXInitial: 0,
			clientXFinal: 0,
			dateDictionary: {
				0: "S",
				1: "M",
				2: "T",
				3: "W",
				4: "T",
				5: "F",
				6: "S",
			},
			deltaDays: 0,
			isMouseDown: false,
			monthArray: [],
			monthDictionary: {
				0: "Jan",
				1: "Feb",
				2: "March",
				3: "April",
				4: "May",
				5: "June",
				6: "July",
				7: "August",
				8: "September",
				9: "October",
				10: "November",
				11: "December",
			},
			spacerWidth: 0,
			startDate: 1712188800000,
			startDateGantt: 1711929600000,
			startDateInitial: 0,
			endDate: 1712361600000,
			endDateGantt: 1720396800000,
		};
	},
	methods: {
		calculateDeltaDays() {
			this.deltaDays =  Math.round((this.endDateGantt - this.startDateGantt) / (1000 * 60 * 60 * 24));
		},
		dragDrop(data) {
			this.clientXFinal = data.clientX;

			//Get the number of dates from this
			let delta = Math.floor((this.clientXFinal - this.clientXInitial) / 35) * (24 * 60 * 60 * 1000);

			//Apply to the start date
			const start_date = new Date(this.startDateGantt + delta);

			//Adjust the start date
			this.startDate = start_date.getTime();

			//Adjust the spacer width
			this.setSpacerWidth();
		},
		dragStart(data) {
			//Setup the inital point of the move
			this.clientXInitial = data.clientX;
		},
		generateHeader() {
			//Blank out month array
			this.monthArray = [];

			//Setup local variables
			let start_date = new Date(this.startDateGantt);
			let end_date = new Date(this.endDateGantt);
			let point_date = start_date;
			let next_date = end_date;

			let keep_looping = true;
			let index = 0;
			while (keep_looping) {
				var delta = 0;

				//Determine if end date is in the current month
				if (point_date.getMonth() === end_date.getMonth()) {
					//Months are the same. Get the delta between the dates and call it a day
					keep_looping = false;

					//Get delta then the width of the object :)
					delta = 1 + Math.round((end_date.getTime() - point_date.getTime()) / (1000 * 60 * 60 * 24));
				} else {
					//Months are different. Get the point date for the first of next month
					if (point_date.getMonth() === 11) {
						//Point date is in December. We want next year
						next_date = new Date(point_date.getFullYear() + 1, 0, 1);
					} else {
						next_date = new Date(point_date.getFullYear(), point_date.getMonth() + 1, 1);
					}

					//Get the delta
					delta = Math.round((next_date.getTime() - point_date.getTime()) / (1000 * 60 * 60 * 24));
				}

				this.monthArray.push({
					index: index,
					delta: delta,
					width: delta * 35,
					month: this.monthDictionary[point_date.getMonth()],
					year: point_date.getFullYear(),
				});

				//Cycle up the variables
				index = index + 1;
				point_date = next_date;

				//ESCAPE IT!!
				//keep_looping = false;
			}
		},
		getDayDate(index) {
			const delta = index * 24 * 60 * 60 * 1000;
			const new_date = new Date(this.startDateGantt + delta);
			return this.dateDictionary[new_date.getDay()];
		},
		getDayText(index) {
			const delta = index * 24 * 60 * 60 * 1000;
			const new_date = new Date(this.startDateGantt + delta);
			return new_date.getDate();
		},
		mouseDown(event) {
			//Get the initial Client X
			this.clientXInitial = event.clientX;

			//Get the inital start date
			this.startDateInitial = this.startDate;

			//Record that the mouse is down
			this.isMouseDown = true;
		},
		mouseLeave() {
			this.isMouseDown = false;
		},
		mouseMove(event) {
			if (this.isMouseDown) {
				this.clientXFinal = event.clientX;


				//Get the number of dates from this
				let delta = Math.floor((this.clientXFinal - this.clientXInitial) / 35) * (24 * 60 * 60 * 1000);

				console.log("Delta: ", delta);

				//Apply to the start date
				const start_date = new Date(this.startDateInitial + delta);

				//Adjust the start date
				this.startDate = start_date.getTime();

				//Adjust the spacer width
				this.setSpacerWidth();
			}
		},
		mouseUp() {
			this.isMouseDown = false;
		},
		setSpacerWidth() {
			let delta = Math.round((this.startDate - this.startDateGantt) / (1000 * 60 * 60 * 24));

			this.spacerWidth = delta * 35;
		},
	},
	mounted() {
		this.calculateDeltaDays();
		this.generateHeader();
		this.setSpacerWidth();
	},
}
</script>

<style>
.gantt-header {
	display: flex;
	flex-direction: row;
	//margin: 50px 0 0 0;
	background-color: lightblue;
}

.gantt-header--information {
	min-width: 200px;
	max-width: 200px;
	background-color: #0a7e5b;
}

.gantt-row {
	display: flex;
	flex-direction: row;
	margin: 0;
	background-color: rgb(105, 50, 50);
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

.gantt-row--date {
	width: 35px;
	//height: 35px;
	background-color: lightgrey;
	border: solid 1px dimgray;
	color: black;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
}

.gantt-row--month {
	background-color: lightblue;
	border: solid 1px lightskyblue;
	color: black;
}

.gantt-row--cells {
	display: flex;
	flex-direction: row;
}

.gantt-row--dates {
	display: flex;
	flex-direction: row;
}

.gantt-row--months {
	display: flex;
	flex-direction: row;
}

.gantt-row--bar {
	background-color: hotpink;
	min-width: 35px;
	width: 70px;
	height: 20px;
	margin-top: 7px;
}

.gantt-row--render-bar {
	position: absolute;
	display: flex;
	flex-direction: row;
}
</style>
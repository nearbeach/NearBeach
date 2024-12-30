<template>
	<div class="gantt-row"
		 id="gantt_row_parent"
	>
		<div class="gantt-row--information"
			 v-on:dragleave="dragleaveRow"
			 v-on:dragover="dragoverRow"
			 v-on:drop="drop"
		>
			<div class="gantt-row--title"></div>
			<div class="gantt-row--start-date"></div>
			<div class="gantt-row--end-date"></div>
			<div class="gantt-row--status"></div>
		</div>

		<div class="gantt-row--render"></div>
	</div>
</template>

<script>
//VueX
import { mapGetters } from "vuex";

//Components
import { Modal } from "bootstrap";

export default {
	name: "RenderBlankGanttRow",
	emits: ['mouse_down'],
	data() {
		return {
			datePickerFormat: "yyyy-MM-dd HH:mm",
			localEndDate: this.endDate,
			localStartDate: this.startDate,
			localStatusId: this.statusId,
			statusList: [],
		};
	},
	computed: {
		...mapGetters({
			//Mouse Down
			mdObjectId: "getMdObjectId",
			mdObjectType: "getMdObjectType",
			mdParentObjectId: "getMdParentObjectId",
			mdParentObjectType: "getMdParentObjectType",
			mdColumn: "getMdColumn",
		}),
	},
	methods: {
		canBeDestination() {
			const exclude_array = [
				null,
				"",
				undefined,
			];

			return !exclude_array.includes(this.mdParentObjectType);
		},
		canObjectMove() {
			//If there are multiple instances of the same object on the sprint, the user can not move this object to
			//the root level. As the object can only be a child element, or root element. Not both at the same time. :)
			const object_list = this.$store.getters.getGanttChartDataByObject(this.mdObjectId, this.mdObjectType);
			return object_list.length <= 1;
		},
		dragleaveRow(event) {
			event.preventDefault();

			const element = document.getElementById("gantt_row_parent");
			element.classList.remove("gantt-chart-row-destination");
		},
		dragoverRow(event) {
			event.preventDefault();

			if (this.canBeDestination() === false) return;

			const element = document.getElementById("gantt_row_parent");
			element.classList.add("gantt-chart-row-destination");
		},
		drop(event) {
			event.preventDefault();

			if (this.canBeDestination() === false) return;

			if (!this.canObjectMove()) {
				this.$store.dispatch("newToast", {
					heading: "Can not move object",
					message: "Sorry object can't be moved, as it isn't the only instance of that object. An object can only exist at root level if it is the only instance",
					extra_classes: "bg-danger",
					delay: 0,
				});

				return;
			}

			const element = document.getElementById("gantt_row_parent");
			element.classList.remove("gantt-chart-row-destination");

			//Handle the process of moving the object :)
			this.$store.dispatch("updateGanttChartSingleRowsParent", {
				object_id: this.mdObjectId,
				object_type: this.mdObjectType,
				parent_object_id: this.mdParentObjectId,
				parent_object_type: this.mdParentObjectType,
				new_parent_object_id: 0,
				new_parent_object_type: "",
			});
		},
	},
}
</script>
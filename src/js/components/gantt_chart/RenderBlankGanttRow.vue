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
			rootUrl: "getRootUrl",

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

			const element = document.getElementById("gantt_row_parent");
			element.classList.remove("gantt-chart-row-destination");

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

			//Handle the process of moving the object :)
			this.$store.dispatch("updateGanttChartSingleRowsParent", {
				object_id: this.mdObjectId,
				object_type: this.mdObjectType,
				parent_object_id: this.mdParentObjectId,
				parent_object_type: this.mdParentObjectType,
				new_parent_object_id: 0,
				new_parent_object_type: "",
			});

			const data_to_remove = new FormData();
			data_to_remove.set("link_id", this.mdObjectId);
			data_to_remove.set("link_connection", this.mdObjectType);

			this.axios.post(
				`${this.rootUrl}object_data/${this.mdParentObjectType}/${this.mdParentObjectId}/remove_link/`,
				data_to_remove,
			).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Failed Updating Sprint",
					message: `Sorry, moving the object failed. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
}
</script>
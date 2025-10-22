<template>
<!--	RENDER THE ONE ELEMENT WE WANT-->
	<render-gantt-row
		:description="description"
		:end-date="endDate"
		:is-closed="isClosed"
		:level-number="levelNumber"
		:object-id="objectId"
		:object-type="objectType"
		:parent-object-id="parentObjectId"
		:parent-object-type="parentObjectType"
		:higher-order-status="higherOrderStatus"
		:sprint-object-assignment-id="sprintObjectAssignmentId"
		:start-date="startDate"
		:status-id="statusId"
		:title="title"
	></render-gantt-row>

<!--	RENDER ALL THE CHILD ELEMENTS WE WANT-->
<!--	TODO: FIX THE "IS-CLOSED", as we have just put false-->
		<render-gantt-group
			v-for="(row, index) in filteredGanttChartData"
			v-if="levelNumber <= 3"
			:key="index"
			:description="row.description"
			:end-date="row.end_date"
			:is-closed="false"
			:level-number="levelNumber + 1"
			:object-id="row.object_id"
			:object-type="row.object_type"
			:parent-object-id="row.parent_object_id"
			:parent-object-type="row.parent_object_type"
			:higher-order-status="row.higher_order_status"
            :sprint-object-assignment-id="row.sprint_object_assignment_id"
			:start-date="row.start_date"
			:status-id="row.status_id"
			:title="row.title"
		></render-gantt-group>
</template>

<script>
import { mapGetters } from "vuex";
import RenderGanttRow from "./RenderGanttRow.vue";

export default {
	name: "RenderGanttGroup",
	components: {RenderGanttRow},
	props: {
		description: {
			type: String,
			default: "",
		},
		endDate: {
			type: Number,
			default: 0,
		},
		higherOrderStatus: {
			type: String,
			default: "",
		},
		isClosed: {
			type: Boolean,
			default: false,
		},
		levelNumber: {
			type: Number,
			default: 0,
		},
		objectId: {
			type: Number,
			default: 0,
		},
		objectType: {
			type: String,
			default: "",
		},
		parentObjectId: {
			type: Number,
			default: 0,
		},
		parentObjectType: {
			type: String,
			default: "",
		},
		sprintObjectAssignmentId: {
			type: Number,
			default: 0,
		},
		startDate: {
			type: Number,
			default: 0,
		},
		statusId: {
			type: Number,
			default: 0,
		},
		title: {
			type: String,
			default: "",
		},
	},
	computed: {
		...mapGetters({
			ganttChartData: "getGanttChartData",
		}),

		filteredGanttChartData() {
			return this.ganttChartData(
				this.objectType,
				this.objectId
			);
		},
	},
	methods: {
	},
}
</script>
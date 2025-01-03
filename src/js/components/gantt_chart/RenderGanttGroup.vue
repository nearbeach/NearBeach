<template>
<!--	RENDER THE ONE ELEMENT WE WANT-->
	<render-gantt-row
		v-bind:description="description"
		v-bind:end-date="endDate"
		v-bind:is-closed="isClosed"
		v-bind:level-number="levelNumber"
		v-bind:object-id="objectId"
		v-bind:object-type="objectType"
		v-bind:parent-object-id="parentObjectId"
		v-bind:parent-object-type="parentObjectType"
		v-bind:higher-order-status="higherOrderStatus"
		v-bind:start-date="startDate"
		v-bind:status-id="statusId"
		v-bind:title="title"
	></render-gantt-row>

<!--	RENDER ALL THE CHILD ELEMENTS WE WANT-->
<!--	TODO: FIX THE "IS-CLOSED", as we have just put false-->
		<render-gantt-group
			v-if="levelNumber <= 3"
			v-for="(row, index) in filteredGanttChartData"
			:key="index"
			v-bind:description="row.description"
			v-bind:end-date="row.end_date"
			v-bind:is-closed="false"
			v-bind:level-number="levelNumber + 1"
			v-bind:object-id="row.object_id"
			v-bind:object-type="row.object_type"
			v-bind:parent-object-id="row.parent_object_id"
			v-bind:parent-object-type="row.parent_object_type"
			v-bind:higher-order-status="row.higher_order_status"
			v-bind:start-date="row.start_date"
			v-bind:status-id="row.status_id"
			v-bind:title="row.title"
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
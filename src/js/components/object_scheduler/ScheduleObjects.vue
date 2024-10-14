<template>
	<div class="card">
		<div class="card-body">
			<h1>Scheduled Objects</h1>
			<hr>

			<div class="alert alert-info"
				 v-if="scheduleObjectResults.length === 0"
			>
				Currently there are no scheduled objects.
			</div>
			<div v-else
 				class="object-card-list"
			>
				<div class="object-card"
					 v-for="result in scheduleObjectResults"
					 :key="result.schedule_object_id"
				>
					<div class="object-card--detail">
						<a v-bind:href="`${rootUrl}scheduled_object_information/${result.schedule_object_id}/`">
							<div class="object-card--detail--link">
								Sch{{ result.schedule_object_id }}<br/>
								<strong>Frequency: </strong> {{ result.frequency }}<br/>
								<strong>Type: </strong> {{ getType(result.object_template_type) }}
							</div>
							<div class="object-card--detail--description">
								{{ result.object_template_json.object_title }}
							</div>
						</a>
					</div>
					<div class="object-card--status">
						<a v-bind:href="`${rootUrl}scheduled_object_information/${result.schedule_object_id}/`">
							<div class="object-card--status--status">
								<span v-if="result.is_active">Active Schedule</span>
								<span v-else>Deactivated</span>
							</div>
						</a>
					</div>
				</div>
			</div>

			<hr v-if="canUserAddScheduledObject">
			<div class="row submit-row"
				v-if="canUserAddScheduledObject"
			>
				<div class="col-md-12">
					<a href="/new_scheduled_object/"
					   class="btn btn-primary save-changes"
					>
						New Scheduled Object
					</a>
				</div>
			</div>

		</div>
	</div>
</template>

<script>
//Mixins
import datetimeMixin from "../../mixins/datetimeMixin";

export default {
	name: "ScheduleObjects",
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
		scheduleObjectResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		userLevel: {
			type: Object,
			default: () => {
				return {
					project: 0,
					task: 0,
				};
			},
		},
	},
	mixins: [
		datetimeMixin,
	],
	computed: {
		canUserAddScheduledObject() {
			//Return if the user level for either project or task is greater than create
			return this.userLevel.project >= 3 || this.userLevel.task >= 3;
		}
	},
	methods: {
		getType(type) {
			if (type === 0 || type === "0") return "Project";

			return "Task";
		},
	},
	mounted() {
	}
}
</script>
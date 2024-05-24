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
			>
				TODO: Add in list
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
		staticUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
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
	computed: {
		canUserAddScheduledObject() {
			//Return if the user level for either project or task is greater than create
			return this.userLevel.project >= 3 || this.userLevel.task >= 3;
		}
	},
	methods: {},
	mounted() {
	}
}
</script>
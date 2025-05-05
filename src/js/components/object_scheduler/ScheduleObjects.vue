<template>
	<div class="card">
		<div class="card-body">
			<h1>Scheduled Objects</h1>
			<hr>

			<!-- SEARCH FIELD -->
			<div class="form-row">
				<div class="form-group">
					<label>Search:</label>
					<input
						type="text"
						class="form-control search-organisation"
						v-model="searchModel"
						maxlength="250"
					/>
				</div>
			</div>
			<hr/>

			<div class="scheduled-object-loader"
				 v-if="isLoadingData"
			>
				<img
					v-bind:src="`${staticUrl}NearBeach/images/placeholder/loading_re.svg`"
					alt="Please wait whilst we load in the scheduled objects"
				/>
			</div>
			<div class="alert alert-info"
				 v-else-if="scheduleObjectResults.length === 0"
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
export default {
	name: "ScheduleObjects",
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
		staticUrl: {
			type: String,
			default: "/",
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
	data() {
		return {
			currentPage: 1,
			isLoadingData: true,
			numberOfPages: 1,
			searchModel: "",
			searchTimeout: "",
			scheduleObjectResults: [],
		}
	},
	computed: {
		canUserAddScheduledObject() {
			//Return if the user level for either project or task is greater than create
			return this.userLevel.project >= 3 || this.userLevel.task >= 3;
		}
	},
	watch: {
		searchModel() {
			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup timer if there are 3 characters or more
			if (this.searchModel.length >= 3 || this.searchModel.length === 0) {
				//Start the potential search
				this.searchTimeout = setTimeout(() => {
					this.getScheduleObjectResults();
				}, 500);
			}
		},
	},
	methods: {
		getScheduleObjectResults() {
			const data_to_send = new FormData();
			data_to_send.set("search", this.searchModel);
			data_to_send.set("array_of_objects", "project");
			data_to_send.set("array_of_objects", "task");
			data_to_send.set("destination_page", this.currentPage);

			this.axios.post(
				`${this.rootUrl}search/scheduled_objects/`,
				data_to_send,
			).then(response => {
				this.scheduleObjectResults = response.data;

				//No longer loading data
				this.isLoadingData = false;
			}).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Error Getting Scheduled Objects",
					message: `Sorry, could not get the scheduled objects. Error -> ${error}`,
					delay: 0,
					extra_classes: "bg-danger",
				});
			});
		},
		getType(type) {
			if (type === 0 || type === "0") return "Project";

			return "Task";
		},
	},
	mounted() {
		this.getScheduleObjectResults();
	}
}
</script>
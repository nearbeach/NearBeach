<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>{{ sprintNameModel }}</h1>
				<a v-bind:href="`${rootUrl}sprint_information/${sprintId}/`"
				>
					Go back to the sprint
				</a>
				<hr/>

				<div class="row">
					<div class="col-md-4">
						<h2>Sprint Title</h2>
						<p class="text-instructions">
							Edit/Update the sprint title, and click "Save" to save the changes.
						</p>
					</div>
					<div class="col-md-8">
						<div class="form-group">
							<label>Sprint Name</label>
							<input
								class="form-control"
								v-model="sprintNameModel"
							/>
						</div>
					</div>
				</div>
				<hr/>

				<div class="row">
					<div class="col-md-4">
						<h2>Sprint Status</h2>
						<p class="text-instructions">
							Use the dropdown to update the sprint status. Can be used to revert any started sprint.
							Click on "Save" to save the changes.
						</p>
					</div>
					<div class="col-md-3">
						<n-select
							v-model:value="sprintStatusModel"
							:options="sprintStatusOptions"
						/>
					</div>
				</div>
				<hr/>

				<between-dates
					destination="Sprint"
					v-bind:start-date-model="sprintStartDateModel.getTime()"
					v-bind:end-date-model="sprintEndDateModel.getTime()"
					v-bind:no-back-dating="false"
					v-on:update_dates="updateDates($event)"
				></between-dates>

				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button
							class="btn btn-primary save-changes"
							v-on:click="saveChanges"
						>
							Save
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";

//Components
import BetweenDates from "../dates/BetweenDates.vue";

//NaiveUi
import {NSelect} from "naive-ui";

export default {
	name: "EditSprint",
	components: {
		BetweenDates,
		NSelect,
	},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
		sprintEndDate: {
			type: String,
			default: "",
		},
		sprintId: {
			type: Number,
			default: 0,
		},
		sprintName: {
			type: String,
			default: "",
		},
		sprintStartDate: {
			type: String,
			default: "",
		},
		sprintStatus: {
			type: String,
			default: "",
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
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			sprintEndDateModel: new Date(this.sprintEndDate),
			sprintNameModel: this.sprintName,
			sprintStartDateModel: new Date(this.sprintStartDate),
			sprintStatusModel: this.sprintStatus,
			sprintStatusOptions: [
				{ value: "Draft", label: "Draft" },
				{ value: "Current", label: "Current" },
				{ value: "Finished", label: "Finished" },
			],
		}
	},
	methods: {
		useNBTheme,
		saveChanges() {
			const data_to_send = new FormData();

			//Set data
			data_to_send.set("sprint_name", this.sprintNameModel);
			data_to_send.set("sprint_status", this.sprintStatusModel);
			data_to_send.set("sprint_start_date", this.sprintStartDateModel.toISOString());
			data_to_send.set("sprint_end_date", this.sprintEndDateModel.toISOString());

			//Notify user of the update
			this.$store.dispatch("newToast", {
				header: "Updating Sprint",
				message: "Please wait, updating sprint",
				extra_classes: "bg-warning",
				delay: 0,
				unique_type: "update_sprint",
			});

			//Axios
			this.axios.post(
				`${this.rootUrl}sprint_information/${this.sprintId}/update_sprint/`,
				data_to_send,
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Updated Sprint",
					message: "Sprint Successfully Updated",
					extra_classes: "bg-success",
					unique_type: "update_sprint",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating Sprint",
					message: `Error updating sprint. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "update_sprint",
				});
			});
		},
		updateDates(event) {
			//Update the start/end date
			this.sprintEndDateModel = new Date(event.end_date);
			this.sprintStartDateModel = new Date(event.start_date);
		},
	},
	mounted() {
		//Send the location id and destination
		this.$store.commit({
			type: "updateDestination",
			destination: "sprint",
			locationId: this.sprintId,
		});

		this.$store.commit({
			type: "updateTitle",
			title: this.sprintName,
		});

		//Send the rootURL to the vuex
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		this.$store.commit({
			type: "updateUserLevel",
			userLevel: this.userLevel,
		});
	}
}
</script>
<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Sprint Information</h1>
				<div class="spacer"></div>
				<a v-bind:href="getParentUrl()">
					Go to Parent Object
				</a>
				<hr>

				<div class="row">
					<div class="col-md-4">
						<strong>Sprint Information</strong>
					</div>
					<div class="col-md-8">
						<p><strong>Sprint Name: </strong> {{ sprintResults[0].sprint_name }}</p>
						<p><strong>Sprint Status: </strong> {{ sprintResults[0].sprint_status }}</p>
						<p><strong>Sprint Start Date: </strong> {{ sprintResults[0].sprint_start_date }}</p>
						<p v-if="sprintResults[0].sprint_status === 'Finish'">
							<strong>Sprint End Date: </strong> {{ sprintResults[0].sprint_end_date }}
						</p>
						<p><strong>Sprint Total Story Points: </strong> {{ sprintResults[0].total_story_points }}</p>
						<p><strong>Sprint Completed Story Points: </strong> {{ sprintResults[0].completed_story_points }}</p>
					</div>
				</div>

				<hr>
				<table class="table table-striped">
					<thead>
						<tr>
							<td>Object</td>
							<td>Description</td>
							<td>Status</td>
						</tr>
					</thead>
					<tbody>
						<tr v-for="item in requirementItemResults"
							:key="item.pk"
						>
							<td>
								<a v-bind:href="`${this.rootUrl}requirement_information/${item.pk}/`">
									Req{{item.pk}}
								</a>
							</td>
							<td>{{item.fields.requirement_item_title}}</td>
							<td>{{item.fields.requirement_item_status}}</td>
						</tr>
						<tr v-for="item in projectResults"
							:key="item.pk"
						>
							<td>
								<a v-bind:href="`${this.rootUrl}project_information/${item.pk}/`">
									Pro{{item.pk}}
								</a>
							</td>
							<td>{{item.fields.project_name}}</td>
							<td>{{item.fields.project_status}}</td>
						</tr>
						<tr v-for="item in taskResults"
							:key="item.pk"
						>
							<td>
								<a v-bind:href="`${this.rootUrl}task_information/${item.pk}/`">
									Task{{item.pk}}
								</a>
							</td>
							<td>{{item.fields.task_short_description}}</td>
							<td>{{item.fields.task_status}}</td>
						</tr>
					</tbody>
				</table>

				<hr>
				<div
					v-if="userLevel >= 2"
					class="row submit-row"
				>
					<div class="col-md-12">
						<button
							v-on:click="showAddObjectWizard"
							class="btn btn-success"
							v-if="sprintResults[0].sprint_status !== 'Finished'"
						>
							Add Object Wizard
						</button>
						<button
							v-on:click="confirmDeleteSprint"
							class="btn btn-danger"
							v-if="sprintResults[0].sprint_status !== 'Finished'"
						>
							Delete
						</button>

						<button
							class="btn btn-success save-changes"
							v-if="sprintResults[0].sprint_status === 'Draft'"
							v-on:click="startSprint"
						>
							Start Sprint
						</button>
						<button
							class="btn btn-warning save-changes"
							v-if="sprintResults[0].sprint_status === 'Current'"
							v-on:click="finishSprint"
						>
							Finish Sprint
						</button>
					</div>
				</div>

			</div>
		</div>

		<confirm-sprint-delete
			v-bind:parent-object-destination="parentObjectDestination"
			v-bind:parent-object-location-id="parentObjectLocationId"
		></confirm-sprint-delete>

		<add-object-wizard></add-object-wizard>
	</n-config-provider>
</template>

<script>
//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";

//Components
import ConfirmSprintDelete from "./ConfirmSprintDelete.vue";
import AddObjectWizard from "./AddObjectWizard.vue";

//Bootstrap
import { Modal } from "bootstrap";

export default {
	name: "SprintInformation",
	components: {
		AddObjectWizard,
		ConfirmSprintDelete,
	},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
		sprintResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		theme: {
			type: String,
			default: "",
		},
		userLevel: {
			type: Number,
			default: 1,
		},

		//TEMP CODE
		requirementItemResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		projectResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		taskResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		//END TEMP CODE
	},
	mixins: [
		getThemeMixin,
	],
	data() {
		return {
			parentObjectDestination: "",
			parentObjectLocationId: 0,
		}
	},
	methods: {
		confirmDeleteSprint() {
			const modal = new Modal(document.getElementById("confirmSprintDeleteModal"));
			modal.show();
		},
		finishSprint() {
			this.axios.post(
				`${this.rootUrl}sprint_information/${this.sprintResults[0].sprint_id}/finish_sprint/`
			).then(() => {
				window.location.reload();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not start sprint",
					message: `Sorry, there was an error starting the sprint. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		getParentUrl() {
			return `${this.rootUrl}${this.parentObjectDestination}_information/${this.parentObjectLocationId}`;
		},
		showAddObjectWizard() {
			const modal = new Modal(document.getElementById("addObjectWizardModal"));
			modal.show();
		},
		startSprint() {
			this.axios.post(
				`${this.rootUrl}sprint_information/${this.sprintResults[0].sprint_id}/start_sprint/`
			).then(() => {
				window.location.reload();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not start sprint",
					message: `Sorry, there was an error starting the sprint. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		//Send data to VueX
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
		});

		this.$store.commit({
			type: "updateDestination",
			destination: "sprint",
			locationId: this.sprintResults[0].sprint_id,
		});

		this.$store.commit({
			type: "updateUserLevel",
			userLevel: this.userLevel,
		});

		//Figure out what destination the parent is and assign the values
		const project = this.sprintResults[0].project;
		const requirement = this.sprintResults[0].requirement;

		//Project
		if (project !== null && project !== undefined && project !== "") {
			this.parentObjectDestination = "project";
			this.parentObjectLocationId = project;
		} else if (requirement !== null && requirement !== undefined && requirement !== "") {
			//Requirement
			this.parentObjectDestination = "requirement";
			this.parentObjectLocationId = requirement;
		} else {
			//We have an issue where we don't know what the parent is. Show error
			this.$store.dispatch("newToast", {
				header: "Error Getting Sprint's Parent",
				message: "We have come across an issue, where the current sprint does not contain a parent!",
				extra_classes: "bg-danger",
				delay: 0,
			});
		}

	}
}
</script>
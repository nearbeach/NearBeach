<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="sprint-header">
			<h1>{{sprintResults[0].sprint_name}}</h1>
			<a v-bind:href="getParentUrl()">
				Go to Parent Object
			</a>
			<div class="spacer"></div>
			<div class="sprint-header--information">
				<div class="sprint-header--information-date"
					 v-if="sprintResults[0].sprint_status === 'Finish'"
				>
					<strong>Finish Date:</strong>
					{{useNiceDatetime(sprintResults[0].sprint_end_date)}}
				</div>
				<div class="sprint-header--information-date"
					 v-else
				>
					<strong>Start Date:</strong>
					{{useNiceDatetime(sprintResults[0].sprint_start_date)}}<br/>
					<strong>End Date:</strong>
					{{useNiceDatetime(sprintResults[0].sprint_end_date)}}
				</div>
				<div class="sprint-header--information-status">
					<strong>Sprint Status:</strong> {{ sprintResults[0].sprint_status }}
				</div>
			</div>

			<hr v-if="userLevel >= 2 && sprintResults[0].sprint_status !== 'Finished'" />
			<div
				v-if="userLevel >= 2"
				class="sprint-header--buttons"
			>
				<button
					v-on:click="showAddObjectWizard"
					class="btn btn-primary"
					v-if="sprintResults[0].sprint_status !== 'Finished'"
				>
					Add Object Wizard
				</button>
				<button
					v-on:click="confirmDeleteSprint"
					class="btn btn-danger delete-button"
					v-if="sprintResults[0].sprint_status !== 'Finished'"
				>
					Delete Sprint
				</button>

				<button
					class="btn btn-success"
					v-if="sprintResults[0].sprint_status === 'Draft'"
					v-on:click="startSprint"
				>
					Start Sprint
				</button>
				<button
					class="btn btn-warning"
					v-if="sprintResults[0].sprint_status === 'Current'"
					v-on:click="finishSprint"
				>
					Finish Sprint
				</button>
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
//Components
import ConfirmSprintDelete from "./ConfirmSprintDelete.vue";
import AddObjectWizard from "./AddObjectWizard.vue";

//Composables
import { useNiceDatetime } from "../../composables/datetime/useNiceDatetime";
import {useNBTheme} from "../../composables/theme/useNBTheme";

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
	},
	data() {
		return {
			parentObjectDestination: "",
			parentObjectLocationId: 0,
		}
	},
	methods: {
		useNBTheme,
		useNiceDatetime,
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
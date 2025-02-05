<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="sprint-header">
			<h1>{{sprintResults[0].sprint_name}}</h1>
			<strong>Sprint Status:</strong> {{ sprintStatus }}
			<div class="dropdown">
				<button class="btn btn-secondary btn-sm dropdown-toggle"
						type="button"
						data-bs-toggle="dropdown"
						aria-expanded="false">
					Sprint Menu
				</button>
				<ul class="dropdown-menu">
					<li>
						<a class="dropdown-item"
						   v-bind:href="getParentUrl()"
						>
							Go to Parent Object
						</a>
					</li>
					<li v-if="userLevel >= 2 && sprintStatus !== 'Finished'">
						<a class="dropdown-item"
						   href="#"
						   v-on:click="showAddObjectWizard"
						>
							Add Object Wizard
						</a>
					</li>
					<li v-if="userLevel >= 2 && (sprintStatus === 'Draft' || sprintStatus === 'Current')">
						<hr class="dropdown-divider">
					</li>
					<li v-if="userLevel >= 2 && sprintStatus === 'Draft'">
						<a class="dropdown-item"
						   href="#"
						   v-on:click="startSprint"
						>
							Start Sprint
						</a>
					</li>
					<li v-if="userLevel >= 2 && sprintStatus === 'Current'">
						<a class="dropdown-item"
						   href="#"
						   v-on:click="finishSprint"
						>
							Finish Sprint
						</a>
					</li>
					<li v-if="userLevel >= 2">
						<hr class="dropdown-divider">
						<a class="dropdown-item"
						   v-bind:href="`${this.rootUrl}sprint_information/${this.sprintId}/edit/`"
						>Edit Sprint</a>
					</li>
					<li v-if="userLevel >= 2 && sprintStatus !== 'Finished'">
						<a class="dropdown-item"
						   href="#"
						   v-on:click="confirmDeleteSprint"
						>
							Delete Sprint
						</a>
					</li>
				</ul>
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
			sprintId: this.sprintResults[0].sprint_id,
			sprintStatus: this.sprintResults[0].sprint_status,
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

		this.$store.commit({
			type: "updateTitle",
			title: this.sprintResults[0].sprint_name,
		});

		//Define what parent object and it's ID is
		const project_id = this.sprintResults[0].project;
		const requirement_id = this.sprintResults[0].requirement_id;
		if (project_id !== null && project_id !== undefined && project_id !== "") {
			this.parentObjectLocationId = project_id;
			this.parentObjectDestination = "project";
		} else if (requirement_id !== null && requirement_id !== undefined && requirement_id !== "") {
			this.parentObjectLocationId = requirement_id;
			this.parentObjectDestination = "requirement";
		}
	},
};
</script>

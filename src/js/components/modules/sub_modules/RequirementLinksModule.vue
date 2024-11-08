<template>
	<div>
		<h2>
			Requirement Links
		</h2>
		<p class="text-instructions">
			The following are links to other projects/tasks. You can link a
			Requirement to these other objects to symbolise a connection between
			the two.
		</p>

		<!-- REQUIREMENT LINKS -->
		<div
			v-if="linkProject.length + linkTask.length === 0"
			class="requirement-item-spacer"
		>
			<div class="alert alert-dark">
				Sorry - there are no Links for this requirement.
			</div>
		</div>
		<div v-else>
			<!-- Project Links -->
			<sub-object-links title="Project Links"
							  v-bind:link-results="linkProject"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>

			<!-- Task Links -->
			<sub-object-links title="Task Links"
							  v-bind:link-results="linkTask"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>
		</div>

		<!-- Submit Button -->
		<div
			v-if="userLevel > 1"
			class="row submit-row"
		>
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="newRequirementLink"
					v-if="userLevel > 1"
				>Create new Link</a
				>
			</div>
		</div>
		<hr/>

		<h2>
			Requirement Item Links
		</h2>
		<p class="text-instructions">
			The following are links for the Items to other projects/tasks.
		</p>

		<!-- ITEM LINKS -->
		<div v-if="itemLinkProject.length + itemLinkTask.length === 0">
			<div class="alert alert-dark">
				Sorry - there are no Item Links. Please navigate to the Item you
				wish to add a link too.
			</div>
		</div>
		<div v-else>
			<!-- Project Links -->
			<sub-object-links title="Project Links"
							  v-bind:link-results="itemLinkProject"
							  v-bind:can-delete="false"
			></sub-object-links>

			<!-- Task Links -->
			<sub-object-links title="Task Links"
							  v-bind:link-results="itemLinkTask"
							  v-bind:can-delete="false"
			></sub-object-links>
		</div>

		<!-- LINKING MODAL -->
		<new-requirement-link-wizard
			v-bind:location-id="locationId"
			destination="requirement"
			v-on:update_module="updateLinkResults"
		></new-requirement-link-wizard>

		<!-- MODAL FOR CONFIRM DELETE LINK -->
		<confirm-link-delete
			v-on:update_link_results="updateLinkResults"
		></confirm-link-delete>
	</div>
</template>

<script>
//JavaScript components
import {Modal} from "bootstrap";

//Components
import NewRequirementLinkWizard from "../wizards/NewRequirementLinkWizard.vue";

//VueX
import {mapGetters} from "vuex";

import SubObjectLinks from "./SubObjectLinks.vue";
import ConfirmLinkDelete from "../wizards/ConfirmLinkDelete.vue";

export default {
	name: "RequirementLinksModule",
	components: {
		ConfirmLinkDelete,
		SubObjectLinks,
		NewRequirementLinkWizard,
	},
	data() {
		return {
			itemLinkProject: [],
			itemLinkTask: [],
			linkProject: [],
			linkTask: [],
			linkModel: [],
		};
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			userLevel: "getUserLevel",
		}),
	},
	methods: {
		newRequirementLink() {
			//Open up the modal
			const elem_modal = new Modal(
				document.getElementById("newRequirementLinkModal")
			);
			elem_modal.show();
		},
		updateLinkResults() {
			//Get the data from the database
			this.axios.post(
				`${this.rootUrl}object_data/requirement/${this.locationId}/object_link_list/`,
			).then((response) => {
				this.linkProject = response.data.filter((row) => {
					return row.object_type === "project";
				});

				this.linkTask = response.data.filter((row) => {
					return row.object_type === "task";
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating Link Results",
					message: `We have had issues updating link results - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			})

			//Get the ITEM links
			this.axios.post(
				`${this.rootUrl}requirement_information/${this.locationId}/data/item_links/`,
			).then((response) => {
				this.itemLinkProject = response.data.filter((row) => {
					return row.object_type === "project";
				}).map((row) => {
					return {
						link_relationship: null,
						parent_link: null,
						object_id: row.object_id,
						object_title: `Item-${row.requirement_item_id} - ${row.object_title}`,
						object_status: row.object_status,
						object_type: row.object_type,
						reverse_relation:false
					};
				});

				this.itemLinkTask = response.data.filter((row) => {
					return row.object_type === "task";
				}).map((row) => {
					return {
						link_relationship: null,
						parent_link: null,
						object_id: row.object_id,
						object_title: `Item-${row.requirement_item_id} - ${row.object_title}`,
						object_status: row.object_status,
						object_type: row.object_type,
						reverse_relation: false
					};
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating Link Results",
					message: `We have had issues updating link results - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		}
	},
	mounted() {
		this.$nextTick(() => {
			this.updateLinkResults();
		});
	},
};
</script>



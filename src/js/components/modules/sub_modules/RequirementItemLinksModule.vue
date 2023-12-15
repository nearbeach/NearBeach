<template>
	<div>
		<h2>
			<Icon v-bind:icon="icons.linkIcon2"></Icon>
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
			<sub-object-links v-bind:title="'Project Links'"
							  v-bind:link-results="itemLinkProject"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>

			<!-- Task Links -->
			<sub-object-links v-bind:title="'Task Links'"
							  v-bind:link-results="itemLinkTask"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>
		</div>

		<!-- Submit Button -->
		<hr v-if="userLevel > 1"/>
		<div
			v-if="userLevel > 1"
			class="row submit-row"
		>
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="newRequirementItemLink"
				>Create new Link</a
				>
			</div>
		</div>

		<!-- LINKING MODAL -->
		<!-- need to build something that resets the requirement links when adding links -->
		<new-requirement-link-wizard
			v-bind:location-id="locationId"
			v-bind:destination="destination"
			v-on:update_module="updateLinkResults($event)"
		></new-requirement-link-wizard>

    <!-- MODAL FOR CONFIRM DELETE LINK -->
    <confirm-link-delete
        v-on:update_link_results="updateLinkResults($event)"
    ></confirm-link-delete>
	</div>
</template>

<script>
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";
import NewRequirementLinkWizard from "../wizards/NewRequirementLinkWizard.vue";
import ConfirmLinkDelete from "../wizards/ConfirmLinkDelete.vue";

//VueX
import {mapGetters} from "vuex";

//Mixins
import iconMixin from "../../../mixins/iconMixin";
import SubObjectLinks from "./SubObjectLinks.vue";

export default {
	name: "RequirementItemLinksModule",
	components: {
    ConfirmLinkDelete,
		Icon,
		NewRequirementLinkWizard,
    SubObjectLinks,
	},
	mixins: [iconMixin],
	data() {
		return {
			// itemLinkResults: [],
      itemLinkProject: [],
      itemLinkTask: [],
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
		updateLinkResults() {
			//Get the data from the database
			this.axios.post(
          		`${this.rootUrl}object_data/requirement_item/${this.locationId}/object_link_list/`,
			).then((response) => {
				this.itemLinkProject = response.data.filter((row) => {
			  		return row.object_type === "project";
				});

				this.itemLinkTask = response.data.filter((row) => {
					return row.object_type === "task";
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating Link Results",
					message: `We have had issues updating link results - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		newRequirementItemLink() {
			//Open up the modal
			const elem_modal = new Modal(
				document.getElementById("newRequirementLinkModal")
			);
			elem_modal.show();
		},
	},
	mounted() {
		//Get the required data we need
    this.$nextTick(() => {
      this.updateLinkResults();
    })
	},
};
</script>

<style scoped></style>

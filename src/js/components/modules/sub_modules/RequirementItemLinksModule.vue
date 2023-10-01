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
import axios from "axios";
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
  inject: [
      'nextTick',
  ],
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
		// extractObjectDescription(link) {
		// 	/*
		// 	The following function will accept a link in. It will then check what that link is connected to. From
		// 	there it will determine which fields it will extract out.
		// 	 */
		// 	var object_description = "ERROR",
		// 		object_id = "ERROR",
		// 		object_link = "/",
		// 		requirement_item_description = "";
    //
		// 	if (link.project_id !== null) {
		// 		object_description = link.project_id__project_name;
		// 		object_id = `Project ${link.project_id}`;
		// 		object_link = `${this.rootUrl}project_information/${link.project_id}`;
		// 	} else if (link.task_id !== null) {
		// 		object_description = link.task_id__task_short_description;
		// 		object_id = `Task ${link.task_id}`;
		// 		object_link = `${this.rootUrl}task_information/${link.task_id}`;
		// 	}
    //
		// 	//Check to see if we need to inser the requirement item description.
		// 	if (link.requirement_id !== null) {
		// 		requirement_item_description = `<p class="requirement-item-link-type">${link.requirement_item_id__requirement_item_title}</p>`;
		// 		object_id = `${object_id} / Item ${link.requirement_id}`;
		// 	}
    //
		// 	//Return the HTML
		// 	return `
    //                 <a href="${object_link}">
    //                     <p>
    //                         ${object_description}
    //                     </p>
    //                     <div class="spacer"></div>
    //                     ${requirement_item_description}
    //                     <p class="requirement-link-type">
    //                         ${object_id}
    //                     </p>
    //                 </a>
    //             `;
		// },
		// extractObjectStatus(link) {
		// 	/*
		// 	The following function will accept a link in. It will then check what that link is connected to. From
		// 	there it will determine what status field it will extract out.
		// 	 */
		// 	var object_status = "ERROR";
    //
		// 	if (link.project_id !== null) {
		// 		object_status = link.project_id__project_status;
		// 	} else if (link.task_id !== null) {
		// 		object_status = link.task_id__task_status;
		// 	}
    //
		// 	return object_status;
		// },
		updateLinkResults() {
			//Get the data from the database
			axios.post(
          `${this.rootUrl}object_data/requirement_item/${this.locationId}/object_link_list/`,
      ).then((response) => {
				// this.itemLinkResults = response.data;
        this.itemLinkProject = response.data.filter((row) => {
          return row.object_type === "project";
        });

        this.itemLinkTask = response.data.filter((row) => {
          return row.object_type === "task";
        });
			});
		},
		newRequirementItemLink() {
			//Open up the modal
			var elem_modal = new Modal(
				document.getElementById("newRequirementLinkModal")
			);
			elem_modal.show();
		},
		// updateModel(data) {
		// 	this.itemLinkResults = data;
		// },
	},
	mounted() {
		//Get the required data we need
    this.nextTick(() => {
      this.updateLinkResults();
    })
	},
};
</script>

<style scoped></style>

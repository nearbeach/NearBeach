<template>
	<div>
		<h2>
			<Icon v-bind:icon="icons.linkOut"></Icon>
			Change Task Links
		</h2>
		<p class="text-instructions">
			The following are links to other change tasks. You can either block
			an existing change task in the future. Or can set it will be Blocked
			by a change task in the past.
		</p>

		<!-- OBJECT LINKS -->
		<div
			v-if="linkResults.length === 0"
			class="requirement-item-spacer"
		>
			<div class="alert alert-dark">
				Sorry - there are no Links for this change task.
			</div>
		</div>
		<div v-else>
			<!-- Is Blocked By -->
			<sub-object-links v-bind:title="'Is Blocked By'"
							  v-bind:link-results="linkResults.filter(row => {return row.link_relationship === 'Block' && row.parent_link !== destination})"
			></sub-object-links>

			<!-- Is Currently Blocking -->
			<sub-object-links v-bind:title="'Is Currently Blocking'"
							  v-bind:link-results="linkResults.filter(row => {return row.link_relationship === 'Block' && row.parent_link === destination})"
			></sub-object-links>
		</div>

		<!-- Submit Button -->
		<div class="row submit-row">
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="newLink"
					v-if="userLevel > 1"
				>Create new Link</a
				>
			</div>
		</div>
		<hr/>

		<!-- MODAL FOR NEW CHANGE TASK LINKS -->
		<new-change-task-link-wizard-vue
			v-on:update_link_results="updateLinkResults"
		></new-change-task-link-wizard-vue>
	</div>
</template>

<script>
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";

//Components
import NewChangeTaskLinkWizardVue from "../../modules/wizards/NewChangeTaskLinkWizard.vue";
import SubObjectLinks from "../../modules/sub_modules/SubObjectLinks.vue";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "ChangeTaskLinkList",
	components: {
		NewChangeTaskLinkWizardVue,
		Icon,
		SubObjectLinks,
	},
	mixins: [iconMixin],
	data() {
		return {
			linkResults: [],
			translateStatus: {
				1: "Draft",
				2: "Waiting for approval",
				3: "Approved",
				4: "Started",
				5: "Finished",
				6: "Rejected",
				7: "Paused",
				8: "Ready for QA",
				9: "Failed",
			}
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
		newLink() {
			//Open up the modal
			const elem_modal = new Modal(
				document.getElementById("newChangeTaskLinkModal")
			);

			elem_modal.show();
		},
		updateLinkResults() {
			//Clear the data
			this.linkResults = [];

			//Get the data from the database
			this.axios.post(
					`${this.rootUrl}object_data/change_task/${this.locationId}/object_link_list/`
      		).then((response) => {
				this.linkResults = response.data.map((row) => {
					//Get results
					let results = row;

					//Mutate the object_status
					results.object_status = this.translateStatus[row.object_status];

					//Return results
					return results;
				})
      		}).catch((error) => {});
		},
	},
	mounted() {
		this.$nextTick(() => {
			setTimeout(() => {
				this.updateLinkResults();
			}, 200);
		});
	},
};
</script>

<style scoped></style>

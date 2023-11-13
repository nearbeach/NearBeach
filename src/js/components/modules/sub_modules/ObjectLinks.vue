<template>
	<div>
		<h2>
			<Icon v-bind:icon="icons.linkOut"></Icon>
			{{ destination }} Links
		</h2>
		<p class="text-instructions">
			The following are links to other objects like
			projects/tasks/requirements. You can link a {{ destination }}
			to these other objects to symbolise a connection between the two.
		</p>

		<!-- OBJECT LINKS -->
		<div
			v-if="linkResults.length === 0"
			class="requirement-item-spacer"
		>
			<div class="alert alert-dark">
				Sorry - there are no Links for this requirement.
			</div>
		</div>
		<div v-else>
			<!-- Relates To -->
			<sub-object-links v-bind:title="'Relates To'"
							  v-bind:link-results="relatesTo"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>

			<!-- Kanban Cards -->
			<sub-object-links v-bind:title="'Kanban Cards'"
							  v-bind:link-results="kanbanCard"
							  v-bind:can-delete="false"
			></sub-object-links>

			<!-- Is Blocked By -->
			<sub-object-links v-bind:title="'Is Blocked By'"
							  v-bind:link-results="isBlockedBy"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>

			<!-- Is Currently Blocking -->
			<sub-object-links v-bind:title="'Is Currently Blocking'"
							  v-bind:link-results="isCurrentlyBlocking"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>

			<!-- Is Sub Object Of -->
			<sub-object-links v-bind:title="'Is Subobject Of'"
							  v-bind:link-results="isSubObjectOf"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>

			<!-- Is Parent Object Of -->
			<sub-object-links v-bind:title="'Is Parent Object Of'"
							  v-bind:link-results="isParentOf"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>

			<!-- Has Duplicate Object Of -->
			<sub-object-links v-bind:title="'Has Duplicate Object Of'"
							  v-bind:link-results="hasDuplicateObjectOf"
							  v-on:update_link_results="updateLinkResults($event)"
			></sub-object-links>

			<!-- Is Duplicate Object Of -->
			<sub-object-links v-bind:title="'Is Duplicate Object Of'"
							  v-bind:link-results="isDuplicateObjectOf"
							  v-on:update_link_results="updateLinkResults($event)"
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

		<!-- MODAL FOR NEW OBJECT LINKS -->
		<new-link-wizard
			v-bind:destination="destination"
			v-bind:location-id="locationId"
			v-on:update_link_results="updateLinkResults"
		></new-link-wizard>

		<!-- MODAL FOR CONFIRM DELETE LINK -->
		<confirm-link-delete
			v-on:update_link_results="updateLinkResults"
		></confirm-link-delete>
	</div>
</template>

<script>
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";

import NewLinkWizard from "../wizards/NewLinkWizard.vue";
import SubObjectLinks from "./SubObjectLinks.vue";
import ConfirmLinkDelete from "../wizards/ConfirmLinkDelete.vue";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "ObjectLinks",
	components: {
		ConfirmLinkDelete,
		Icon,
		NewLinkWizard,
		SubObjectLinks,
	},
	mixins: [iconMixin],
	data() {
		return {
			hasDuplicateObjectOf: [],
			isBlockedBy: [],
			isCurrentlyBlocking: [],
			isDuplicateObjectOf: [],
			isParentOf: [],
			isSubObjectOf: [],
			kanbanCard: [],
			linkResults: [],
			relatesTo: [],
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
		isLinkedObject(object) {
			let results = false;

			if (object.fields.project !== null) results = true;
			if (object.fields.task !== null) results = true;
			if (object.fields.requirement !== null) results = true;

			return results;
		},
		newLink() {
			//Open up the modal

			const elem_modal = new Modal(
				document.getElementById("newLinkModal")
			);

			elem_modal.show();
		},
		updateLinkResults() {
			//Clear the data
			this.linkResults = [];

			//Get the data from the database
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/object_link_list/`
			).then((response) => {
				this.linkResults = response.data

				//Filter out the data for relates to
				this.relatesTo = response.data.filter(row => {
					//We only have one condition - if there is a relate
					return row.link_relationship === 'Relate' || row.link_relationship === null;
				});

				//Filter out the data for is blocked by
				this.isBlockedBy = response.data.filter(row => {
					const condition_1 = row.link_relationship === 'Block' && row.parent_link !== this.destination && row.reverse_relation === false;
					const condition_2 = row.link_relationship === 'Block' && row.parent_link === this.destination && row.reverse_relation === true; //reverse
					return condition_1 || condition_2;
				})

				//Filter out the data for kanban cards
				this.kanbanCard = response.data.filter(row => {
					//We only have one condition - if there is a kanban card
					return row.link_relationship === 'Card'
				})

				//Filter out the data for is currently blocking
				this.isCurrentlyBlocking = response.data.filter(row => {
					const condition_1 = row.link_relationship === 'Block' && row.parent_link === this.destination && row.reverse_relation === false;
					const condition_2 = row.link_relationship === 'Block' && row.parent_link !== this.destination && row.reverse_relation === true; //reverse
					return condition_1 || condition_2;
				})

				//Filter out the dat for is subobject of
				this.isSubObjectOf = response.data.filter(row => {
					const condition_1 = row.link_relationship === 'Subobject' && row.parent_link !== this.destination && row.reverse_relation === false;
					const condition_2 = row.link_relationship === 'Subobject' && row.parent_link === this.destination && row.reverse_relation === true;
					return condition_1 || condition_2;
				})

				this.isParentOf = response.data.filter(row => {
					const condition_1 = row.link_relationship === 'Subobject' && row.parent_link === this.destination && row.reverse_relation === false;
					const condition_2 = row.link_relationship === 'Subobject' && row.parent_link !== this.destination && row.reverse_relation === true;
					return condition_1 || condition_2;
				})

				this.hasDuplicateObjectOf = response.data.filter(row => {
					const condition_1 = row.link_relationship === 'Duplicate' && row.parent_link === this.destination && row.reverse_relation === false;
					const condition_2 = row.link_relationship === 'Duplicate' && row.parent_link !== this.destination && row.reverse_relation === true;
					return condition_1 || condition_2;
				})

				this.isDuplicateObjectOf = response.data.filter(row => {
					const condition_1 = row.link_relationship === 'Duplicate' && row.parent_link !== this.destination && row.reverse_relation === false;
					const condition_2 = row.link_relationship === 'Duplicate' && row.parent_link === this.destination && row.reverse_relation === true;
					return condition_1 || condition_2;
				})
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					heading: "Object Links failed to get data",
					message: `Failed to get data - Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.updateLinkResults();
		});
	},
};
</script>

<style scoped></style>

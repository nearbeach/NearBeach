<template>
	<div>
		<h2>
			<Icon v-bind:icon="icons.linkOut"></Icon> {{ destination }} Links
		</h2>
		<p class="text-instructions">
			The following are links to other objects like
			projects/tasks/requirements. You can link a {{ destination }}
			to these other objects to symbolise a connection between the two.
		</p>

		<!-- OBJECT LINKS -->
		<div
			v-if="linkResults.length == 0"
			class="requirement-item-spacer"
		>
			<div class="alert alert-dark">
				Sorry - there are no Links for this requirement.
			</div>
		</div>
		<div v-else>
			<!-- Relates To -->
			<sub-object-links v-bind:title="'Relates To'"
				v-bind:link-results="linkResults.filter(row => {return row.link_relationship === 'Relate'})"
				v-on:update_link_results="updateLinkResults"
			></sub-object-links>

			<!-- Is Blocked By -->
			<sub-object-links v-bind:title="'Is Blocked By'"
				v-bind:link-results="linkResults.filter(row => {return row.link_relationship === 'Block' && row.parent_link !== destination})"
				v-on:update_link_results="updateLinkResults"
			></sub-object-links>

			<!-- Is Currently Blocking -->
			<sub-object-links v-bind:title="'Is Currently Blocking'"
				v-bind:link-results="linkResults.filter(row => {return row.link_relationship === 'Block' && row.parent_link === destination})"
				v-on:update_link_results="updateLinkResults"
			></sub-object-links>
			
			<!-- Is Sub Object Of -->
			<sub-object-links v-bind:title="'Is Subobject Of'"
				v-bind:link-results="linkResults.filter(row => {return row.link_relationship === 'Subobject' && row.parent_link !== destination})"
				v-on:update_link_results="updateLinkResults"
			></sub-object-links>

			<!-- Is Parent Object Of -->
			<sub-object-links v-bind:title="'Is Parent Object Of'"
				v-bind:link-results="linkResults.filter(row => {return row.link_relationship === 'Subobject' && row.parent_link === destination})"
				v-on:update_link_results="updateLinkResults"
			></sub-object-links>

			<!-- Has Duplicate Object Of -->
			<sub-object-links v-bind:title="'Has Duplicate Object Of'"
				v-bind:link-results="linkResults.filter(row => {return row.link_relationship === 'Duplicate' && row.parent_link === destination})"
				v-on:update_link_results="updateLinkResults"
			></sub-object-links>

			<!-- Is Duplicate Object Of -->
			<sub-object-links v-bind:title="'Is Duplicate Object Of'"
				v-bind:link-results="linkResults.filter(row => {return row.link_relationship === 'Duplicate' && row.parent_link !== destination})"
				v-on:update_link_results="updateLinkResults"
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
		<hr />

		<!-- MODAL FOR NEW OBJECT LINKS -->
		<new-link-wizard
			v-bind:destination="destination"
			v-bind:location-id="locationId"
			v-on:update_link_results="updateLinkResults"
		></new-link-wizard>
	</div>
</template>

<script>
	import { Modal } from "bootstrap";
	import { Icon } from "@iconify/vue";
	const axios = require("axios");
	import NewLinkWizard from "../wizards/NewLinkWizard.vue";
	import SubObjectLinks from "./SubObjectLinks.vue";

	//Mixins
	import iconMixin from "../../../mixins/iconMixin";

	//VueX
	import { mapGetters } from "vuex";

	export default {
		name: "ObjectLinks",
		components: {
			Icon,
			NewLinkWizard,
			SubObjectLinks,
		},
		mixins: [iconMixin],
		data() {
			return {
				linkResults: [],
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

				var elem_modal = new Modal(
					document.getElementById("newLinkModal")
				);

				elem_modal.show();
			},
			updateLinkResults() {
				//Clear the data
				this.linkResults = [];

				//Get the data from the database
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/object_link_list/`
					)
					.then((response) => {
						this.linkResults = response.data
					});
			},
		},
		mounted() {
			//Wait 200ms before getting data
			setTimeout(() => {
				this.updateLinkResults();
			}, 200);
		},
	};
</script>

<style scoped></style>

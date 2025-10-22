<template>
	<div>
		<h2>
			Requirement Items
		</h2>
		<p class="text-instructions">
			Requirements should be broken down into smaller components called
			Requirement Items.
		</p>

		<!-- TABLE OF REQUIREMENT ITEMS -->
		<div
			v-if="itemResults.length === 0"
			class="requirement-item-spacer"
		>
			<div class="alert alert-dark">
				Sorry - there are no Items for this requirement.
			</div>
		</div>
		<div v-else>
			<render-object-card
:import-variables="requirementItemVariables"
								:search-results="itemResults"
								destination="requirement_item"
			></render-object-card>
		</div>

		<!-- Submit Button -->
		<!-- TO DO - limit it to certain users -->
		<hr v-if="userLevel > 1"/>
		<div
			v-if="userLevel > 1"
			class="row submit-row"
		>
			<div class="col-md-12">
				<button
					class="btn btn-primary save-changes"
					@click="createNewItem"
				>
					Create new Requirement Item
				</button>
			</div>
		</div>

		<!-- NEW REQUIREMENT ITEM MODAL -->
		<new-requirement-item-wizard
			:item-status-list="itemStatusList"
			:item-type-list="itemTypeList"
			:location-id="locationId"
			@new_item_added="newItemAdded($event)"
		></new-requirement-item-wizard>
	</div>
</template>

<script>
//JavaScript Libraries
import {Modal} from "bootstrap";

//Components
import NewRequirementItemWizard from "../wizards/NewRequirementItemWizard.vue";
import RenderObjectCard from "Components/render/RenderObjectCard.vue";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "RequirementItemsModule",
	components: {
		RenderObjectCard,
		NewRequirementItemWizard,
	},
	data() {
		return {
			requirementItemVariables: {
				header: "Requirement Items",
				prefix: "RI-",
				id: "requirement_item_id",
				title: "requirement_item_title",
				status: "requirement_item_status_text",
				end_date: "",
			},
			itemResults: [],
			itemStatusList: [],
			itemTypeList: [],
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
	mounted() {
		this.updateItemResults();
	},
	methods: {
		createNewItem() {
			const new_item_modal = new Modal(
				document.getElementById("newItemModal")
			);
			new_item_modal.show();
		},
		newItemAdded(data) {
			//A new item has been added in the wizard. We use the new data that has passed through to update
			//the item results array.
			this.itemResults = data;
		},
		updateItemResults() {
			this.axios.post(
				"data/items/"
			).then((response) => {
				this.itemResults = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating Item Results",
					message: `We are having issues updating item results: Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
};
</script>



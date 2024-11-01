<template>
	<div class="card">
		<div class="card-body">
			<h2>Requirement Items</h2>
			<p class="text-instructions">
				Requirements should be broken down into smaller components called
				Requirement Items.
			</p>

			<!-- TABLE OF REQUIREMENT ITEMS -->
			<div
				v-if="requirementItemResults.length === 0"
				class="requirement-item-spacer"
			>
				<div class="alert alert-dark">
					Sorry - there are no Items for this requirement.
				</div>
			</div>
			<div v-else>
				<div class="object-card-list">
					<div class="object-card"
						 v-for="result in requirementItemResults"
						 :key="result.pk"
					>
						<div class="object-card--detail">
							<a href="javascript:void(0)"
							   v-on:click="requirementItemClicked(result)"
							>
								<div class="object-card--detail--link">
									RI-{{ result.pk}}
								</div>
								<div class="object-card--detail--description">
									{{ result.fields.requirement_item_title }}
								</div>
							</a>
						</div>
						<div class="object-card--status">
							<div class="object-card--status--status">
								{{ getStatus(result.fields.requirement_item_status) }}
							</div>
							<p class="small-text">
								{{ useNiceDatetime(result.fields.requirement_item_end_date) }}
							</p>
						</div>
					</div>
				</div>
			</div>

			<!-- REQUIREMENT ITEM MODAL -->
			<public-requirement-item-information
				v-bind:requirement-item-results="selectedReqirementItem"
				v-bind:organisation-results="organisationResults"
				v-bind:default-stakeholder-image="defaultStakeholderImage"
				v-bind:status-list="statusList"
				v-bind:type-list="typeList"
			></public-requirement-item-information>
		</div>
	</div>

</template>

<script>
import { Modal } from "bootstrap";

//VueX
import { mapGetters } from "vuex";

//Components
import PublicRequirementItemInformation from "./public_requirement_item_information.vue";

//Composables
import {useNiceDatetime} from "../../composables/datetime/useNiceDatetime";

export default {
	name: "PublicRequirementItemList",
	components: {
		PublicRequirementItemInformation,
	},
	props: {
		requirementItemResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		organisationResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		defaultStakeholderImage: {
			type: String,
			default: "/",
		},
		statusList: {
			type: Array,
			default: () => {
				return [];
			},
		},
		typeList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	data: () => ({
		selectedReqirementItem: [],
	}),
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			rootUrl: "getRootUrl",
			skin: "getSkin",
			staticUrl: "getStaticUrl",
			userLevel: "getUserLevel",
			theme: "getTheme",
		}),
		getStakeholderImage() {
			const image =
				this.stakeholderModel.organisation_profile_picture;
			if (image === "" || image === null) {
				//There is no image - return the default image
				return this.defaultStakeholderImage;
			}
			return `${this.rootUrl}private/${this.stakeholderModel.organisation_profile_picture}`;
		},
	},
	methods: {
		useNiceDatetime,
		getStatus(status) {
			//Filter for the status
			const filtered_status = this.statusList.filter((row) => {
				return parseInt(row.pk) === parseInt(status);
			})

			if (filtered_status.length === 0)
			{
				//Don't know the status
				return "Unknown";
			}

			return filtered_status[0].fields.requirement_item_status;
		},
		requirementItemClicked(result) {
			//Update the selected requirement item
			this.selectedReqirementItem = [result];

			//Open the modal
			const modal = new Modal(
				document.getElementById("item_modal")
			);
			modal.show();
		}
	},
}
</script>
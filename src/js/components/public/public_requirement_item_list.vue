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
							<div class="object-card--detail--link">
								RI-{{ result.pk}}
							</div>
							<div class="object-card--detail--description">
								{{ result.fields.requirement_item_title }}
							</div>
						</div>
						<div class="object-card--status">
							<div class="object-card--status--status">
								{{ result.fields.requirement_item_status }}
							</div>
							<p class="small-text">
								{{ getNiceDate(result.fields.requirement_item_end_date) }}
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import { mapGetters } from "vuex";

//Mixins
import dateTimeMixin from "../../mixins/datetimeMixin"

export default {
	name: "PublicRequirementItemList",
	mixins: [dateTimeMixin],
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
}
</script>
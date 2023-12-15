<template>
	HELLO WORLD - MODAL from RequirementItemInformation
</template>

<script>
import {mapGetters} from "vuex";

export default {
	name: "PublicRequirementItemInformation",
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
		theme: {
			type: String,
			default: ""
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
	mounted() {
		//Map the original lists to something NSelect can read
		this.statusFixList = this.statusList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.requirement_item_status,
			};
		});

		this.typeFixList = this.typeList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.requirement_item_type,
			};
		});
	},
}
</script>
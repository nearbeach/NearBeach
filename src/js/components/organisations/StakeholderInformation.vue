<template>
	<div class="row">
		<!-- Description -->
		<div class="col-md-4">
			<h2>Stakeholder</h2>
		</div>
		<div class="col-md-8 organisation-details">
			<img
				v-bind:src="getStakeholderImage"
				alt="Stakeholder Logo"
				class="organisation-image"
			/>
			<div class="organisation-name">
				<a
					v-bind:href="`${rootUrl}organisation_information/${organisationResults[0].pk}/`"
				>
					{{ stakeholderModel.organisation_name }}
				</a>
			</div>
			<div class="organisation-link">
				<carbon-link></carbon-link>
				Website:
				<a
					v-bind:href="stakeholderModel.organisation_website"
					target="_blank"
					rel="noopener noreferrer"
				>
					{{ stakeholderModel.organisation_website }}
				</a>
			</div>
			<div class="organisation-email">
				<carbon-email></carbon-email>
				Email:
				<a
					v-bind:href="`mailto:${stakeholderModel.organisation_email}`"
				>
					{{ stakeholderModel.organisation_email }}
				</a>
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";
import {CarbonEmail, CarbonLink} from "../../components";

export default {
	name: "StakeholderInformation",
	components: {
		CarbonEmail,
		CarbonLink,
	},
	props: {
		defaultStakeholderImage: {
			type: String,
			default: "",
		},
		organisationResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	data() {
		return {
			stakeholderModel: this.organisationResults[0].fields,
		};
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
		}),
		getStakeholderImage() {
			const image =
				this.stakeholderModel.organisation_profile_picture;
			if (image === "" || image === null) {
				//There is no image - return the default image
				return this.defaultStakeholderImage;
			}
			return `${this.rootUrl}private/${image}`;
		},
	},
};
</script>



<template>
	<div v-for="organisation in organisationResults"
		 :key="organisation.id"
		 class="organisation-details">
		<img
			v-bind:src="getProfilePicture(organisation)"
			alt="Stakeholder Logo"
			class="organisation-image"
		/>
		<div class="organisation-name">
			<a
				v-bind:href="`${rootUrl}organisation_information/${organisation.pk}/`"
			>
				{{ organisation.fields.organisation_name }}
			</a>
		</div>
		<div class="organisation-link">
			<carbon-link></carbon-link>
			Website:
			<a
				v-bind:href="organisation.fields.organisation_website"
				target="_blank"
				rel="noopener noreferrer"
			>
				{{ organisation.fields.organisation_website }}
			</a>
		</div>
		<div class="organisation-email">
			<carbon-email></carbon-email>
			Email:
			<a
				v-bind:href="`mailto:${organisation.fields.organisation_email}`"
			>
				{{ organisation.fields.organisation_email }}
			</a>
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";
import {CarbonEmail, CarbonLink} from "../../components";

export default {
	name: "ListOrganisations",
	components: {
		CarbonEmail,
		CarbonLink,
	},
	props: {
		organisationResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
		}),
	},
	methods: {
		getProfilePicture(organisation) {
			const image = organisation.fields.organisation_profile_picture;

			//If customer profile is blank - return default picture
			if (image === "" || image === null) {
				return `${this.staticUrl}NearBeach/images/placeholder/product_tour.svg`;
			}

			return `${this.rootUrl}private/${image}`;
		},
	},
};
</script>



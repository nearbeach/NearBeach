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
			<Icon v-bind:icon="icons.linkOut"></Icon>
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
			<Icon v-bind:icon="icons.mailIcon"></Icon>
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
import {Icon} from "@iconify/vue";

//Mixins
import iconMixin from "../../mixins/iconMixin";

export default {
	name: "ListOrganisations",
	components: {
		Icon,
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
	mixins: [iconMixin],
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

<style scoped></style>

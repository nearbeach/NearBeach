<template>
	<div
		v-for="customer in customerResults"
		v-bind:key="customer.pk"
		class="customer-details">
		<img
			v-bind:src="getProfilePicture(customer)"
			alt="Stakeholder Logo"
			class="customer-image"
		/>
		<div class="customer-name">
			<a
				v-bind:href="`${rootUrl}customer_information/${customer.pk}/`"
			>
				{{ customer.fields.customer_first_name }}
				{{ customer.fields.customer_last_name }}
			</a>
		</div>
		<div class="customer-email">
			<carbon-email></carbon-email>
			Email:
			<a v-bind:href="`mailto:${customer.fields.customer_email}`">
				{{ customer.fields.customer_email }}
			</a>
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";
import {CarbonEmail} from "../../components";

export default {
	name: "ListCustomers",
	components: {
		CarbonEmail,
	},
	props: {
		customerResults: {
			type: Array,
			default() {
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
		getProfilePicture(customer) {
			const image = customer.fields.customer_profile_picture;

			//If customer profile is blank - return default picture
			if (image === "" || image === null) {
				return `${this.staticUrl}NearBeach/images/placeholder/product_tour.svg`;
			}

			return `${this.rootUrl}private/${image}`;
		},
	},
};
</script>



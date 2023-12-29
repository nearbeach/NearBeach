<template>
	<div class="customer-list">
		<div
			v-for="customer in customerResults"
			:key="customer.pk"
			class="customer-card"
		>
			<!-- CUSOMER PROFILE -->
			<img
				v-bind:src="getCustomerImage(customer)"
				alt="default profile picture"
			/>

			<!-- CUSTOMER DETAILS -->
			<div class="customer-card--details">
				<div class="customer-card--name">
					<a
						v-bind:href="`${rootUrl}customer_information/${customer.pk}/`"
					>
						{{ customer.fields.customer_first_name }}
						{{ customer.fields.customer_last_name }}
					</a>
				</div>
				<div class="customer-card--email">
					<Icon v-bind:icon="icons.mailIcon"></Icon>
					{{ customer.fields.customer_email }}
				</div>
			</div>

			<div
				class="customer-card--remove"
				v-if="userLevel >= 2"
			>
				<Icon
					v-bind:icon="icons.trashCan"
					v-on:click="removeCustomer(customer.pk)"
				/>
			</div>
		</div>
	</div>
</template>

<script>
import {Icon} from "@iconify/vue";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "CustomersListModule",
	components: {
		Icon,
	},
	props: {
		customerResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
			userLevel: "getUserLevel",
		}),
		defaultCustomerImage() {
			return `${this.staticUrl}/NearBeach/images/placeholder/people_tax.svg`;
		},
	},
	mixins: [iconMixin],
	data() {
		return {};
	},
	methods: {
		getCustomerImage(customer) {
			const image = customer.fields.customer_profile_picture;

			if (image === "" || image === null) {
				//There is no image - return the default image
				return this.defaultCustomerImage;
			}
			return `${this.rootUrl}private/${image}`;
		},
		removeCustomer(customer_id) {
			//Setup data_to_send
			const data_to_send = new FormData();
			data_to_send.set("customer_id", customer_id);

			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_customer/`,
				data_to_send,
			).then(() => {
				//Filter out the delete customer
				this.$emit("remove_customer", customer_id);
			})
		},
	},
};
</script>

<style scoped></style>

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
					v-on:click="confirmRemoveCustomer(customer.pk)"
				/>
			</div>
		</div>
	</div>

	<confirm-customer-removal
		v-bind:customer-object="customerObject"
		v-on:remove_customer="removeCustomer($event)"
	></confirm-customer-removal>
</template>

<script>
import { Modal } from "bootstrap";
import {Icon} from "@iconify/vue";
import ConfirmCustomerRemoval from "../wizards/ConfirmCustomerRemove.vue";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "CustomersListModule",
	components: {
		ConfirmCustomerRemoval,
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
		return {
			customerObject: {
				customer_id: 0,
				customer_email: "",
				customer_first_name: "",
				customer_last_name: "",
				customer_profile_picture: "",
			},
		};
	},
	emits: ["remove_customer"],
	methods: {
		confirmRemoveCustomer(customer_id) {
			//Update the customer object
			const customer_object = this.customerResults.filter((row) => {
				return parseInt(row.pk) === parseInt(customer_id);
			});

			if (customer_object.length !== 1) {
				//Something went wrong. Notify the user and do nothing.
				this.$store.dispatch("newToast", {
					header: "Error Deleting Customer",
					message: "Could not select the correct ID of the customer. Something went wrong",
					extra_classes: "bg-danger",
					delay: 0,
				});

				return;
			}

			//Map the data into a flat pack. As we only require this data
			this.customerObject = customer_object.map(row => {
				return {
					customer_id: row.pk,
					customer_email: row.fields.customer_email,
					customer_first_name: row.fields.customer_first_name,
					customer_last_name: row.fields.customer_last_name,
					customer_profile_picture: row.fields.customer_profile_picture,
				};
			})[0];

			//Show the modal
			const modal = new Modal(document.getElementById("confirmCustomerRemoveModal"));
			modal.show();
		},
		getCustomerImage(customer) {
			const image = customer.fields.customer_profile_picture;

			if (image === "" || image === null) {
				//There is no image - return the default image
				return this.defaultCustomerImage;
			}
			return `${this.rootUrl}private/${image}`;
		},
		removeCustomer(customer_id) {
			//Notify upstream
			this.$emit("remove_customer", customer_id);
		},
	},
};
</script>

<style scoped></style>

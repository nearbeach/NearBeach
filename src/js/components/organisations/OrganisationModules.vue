<template>
  <n-config-provider :theme="getTheme(theme)">
  <div class="card">
		<div class="card-body">
			<!-- The MENU Items -->
			<ul
				class="nav nav-tabs"
				id="misc_module_tabs"
				role="tablist"
			>
				<!-- Organisation Contacts -->
				<li
					class="nav-item"
					role="presentation"
				>
					<button
						class="nav-link"
						id="organisation-contacts-tab"
						data-bs-toggle="tab"
						data-bs-target="#organisation-contacts"
						type="button"
						role="tab"
						aria-controls="home"
						aria-selected="true"
					>
						Organisation Contacts
					</button>
				</li>

				<!-- Document Uploads -->
				<li
					class="nav-item"
					role="presentation"
				>
					<button
						class="nav-link"
						id="document-uploads-tab"
						data-bs-toggle="tab"
						data-bs-target="#document-uploads"
						type="button"
						role="tab"
						aria-controls="home"
						aria-selected="true"
					>
						Document Uploads
					</button>
				</li>

				<!-- Associated Projects & Tasks -->
				<li
					class="nav-item"
					role="presentation"
				>
					<button
						class="nav-link"
						id="associated-objects-tab"
						data-bs-toggle="tab"
						data-bs-target="#associated-objects"
						type="button"
						role="tab"
						aria-controls="home"
						aria-selected="true"
					>
						Associated Objects
					</button>
				</li>

				<!-- Misc Modules -->
				<li
					class="nav-item"
					role="presentation"
				>
					<button
						class="nav-link"
						id="misc-modules-tab"
						data-bs-toggle="tab"
						data-bs-target="#misc-modules"
						type="button"
						role="tab"
						aria-controls="home"
						aria-selected="true"
					>
						Misc
					</button>
				</li>

				<!-- Notes Modules -->
				<li
					class="nav-item"
					role="presentation"
				>
					<button
						class="nav-link"
						id="notes-modules-tab"
						data-bs-toggle="tab"
						data-bs-target="#notes-modules"
						type="button"
						role="tab"
						aria-controls="home"
						aria-selected="true"
					>
						Notes
					</button>
				</li>
			</ul>
			<hr />

			<!-- The Modules -->
			<div
				class="tab-content"
				id="misc_module_content"
			>
				<div
					class="tab-pane fade"
					id="organisation-contacts"
					role="tabpanel"
					aria-labelledby="profile-tab"
				>
					<h2><Icon v-bind:icon="icons.userIcon"></Icon> Contacts</h2>
					<p class="text-instructions">
						Below are a list of contacts who are connected to this
						organisation.
					</p>
					<customers-list-module
						v-bind:customer-results="customerResults"
					></customers-list-module>

					<!-- ADD CUSTOMER BUTTON -->
					<!-- ADD IN PERMISSIONS -->
					<hr v-if="userLevel > 1" />
					<div
						v-if="userLevel > 1"
						class="row submit-row"
					>
						<div class="col-md-12">
							<button
								class="btn btn-primary save-changes"
								v-on:click="addNewContact"
							>
								Add Contact
							</button>
						</div>
					</div>
				</div>
				<div
					class="tab-pane fade"
					id="document-uploads"
					role="tabpanel"
					aria-labelledby="profile-tab"
				>
					<documents-module
						v-bind:destination="destination"
						v-bind:location-id="locationId"
					></documents-module>
				</div>
				<div
					class="tab-pane fade"
					id="associated-objects"
					role="tabpanel"
					aria-labelledby="profile-tab"
				>
					<associated-objects
					></associated-objects>
				</div>
				<div
					class="tab-pane fade"
					id="misc-modules"
					role="tabpanel"
					aria-labelledby="profile-tab"
				>
					<list-tags-module></list-tags-module>
				</div>
				<div
					class="tab-pane fade"
					id="notes-modules"
					role="tabpanel"
					aria-labelledby="profile-tab"
				>
					<notes-module
						v-bind:location-id="locationId"
						v-bind:destination="destination"
					></notes-module>
				</div>
			</div>
		</div>

		<!-- MODALS -->
		<new-customer-modal
			v-bind:organisation-id="locationId"
			v-bind:title-list="titleList"
		></new-customer-modal>
	</div>
  </n-config-provider>
</template>

<script>
	import { Modal } from "bootstrap";
	import { Icon } from "@iconify/vue";
	import CustomersListModule from "../modules/sub_modules/CustomersListModule.vue";
	import ListTagsModule from "../modules/sub_modules/ListTagsModule.vue";
	import NewCustomerModal from "../customers/NewCustomerModal.vue";
	import NotesModule from "../modules/sub_modules/NotesModule.vue";
	import AssociatedObjects from "../modules/sub_modules/AssociatedObjects.vue";
	import DocumentsModule from "../modules/sub_modules/DocumentsModule.vue";

	//VueX
	// import { mapGetters } from 'vuex';

	//Mixins
  import getThemeMixin from "../../mixins/getThemeMixin";
	import iconMixin from "../../mixins/iconMixin";

	export default {
		name: "OrganisationModules",
		components: {
			AssociatedObjects,
			CustomersListModule,
			DocumentsModule,
			Icon,
			ListTagsModule,
			NewCustomerModal,
			NotesModule,
		},
		props: {
			customerResults: {
				type: Array,
				default: () => {
					return [];
				},
			},
			destination: {
				type: String,
				default: "",
			},
			locationId: {
				type: Number,
				default: 0,
			},
			staticUrl: {
				type: String,
				default: "/",
			},
			rootUrl: {
				type: String,
				default: "/",
			},
      theme: {
        type: String,
        default: "",
      },
			titleList: {
				type: Array,
				default: () => {
					return [];
				},
			},
			userLevel: {
				type: Number,
				default: 0,
			},
		},
		computed: {
			// ...mapGetters({
			//     userLevel: 'getUserLevel',
			// }),
		},
		mixins: [getThemeMixin, iconMixin],
		methods: {
			addNewContact() {
				var new_customer_modal = new Modal(
					document.getElementById("addCustomerModal")
				);
				new_customer_modal.show();
			},
		},
		mounted() {
			//Send the ROOT URL and STATIC URL upstream
			this.$store.commit({
				type: "updateUrl",
				staticUrl: this.staticUrl,
				rootUrl: this.rootUrl,
			});

			//Send the user permissions to VUEX
			this.$store.commit({
				type: "updateUserLevel",
				userLevel: this.userLevel,
			});

			//Send the destination and location to VUEX
			this.$store.commit({
				type: "updateDestination",
				destination: this.destination,
				locationId: this.locationId,
			})
		},
	};
</script>

<style scoped></style>

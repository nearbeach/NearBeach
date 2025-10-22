<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<!-- The MENU Items -->
				<ul
					id="misc_module_tabs"
					class="nav nav-tabs"
					role="tablist"
				>
					<!-- Organisation Contacts -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							id="organisation-contacts-tab"
							class="nav-link"
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
							id="document-uploads-tab"
							class="nav-link"
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
							id="associated-objects-tab"
							class="nav-link"
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
							id="misc-modules-tab"
							class="nav-link"
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
							id="notes-modules-tab"
							class="nav-link"
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

					<!-- ADMIN -->
					<li
						v-if="userLevel === 4"
						class="nav-item"
						role="presentation"
					>
						<button
							id="admin-tab"
							class="nav-link"
							data-bs-toggle="tab"
							data-bs-target="#admin"
							type="button"
							role="tab"
							aria-controls="home"
							aria-select="false"
						>
							Admin
						</button>
					</li>
				</ul>
				<hr/>

				<!-- The Modules -->
				<div
					id="misc_module_content"
					class="tab-content"
				>
					<div
						id="organisation-contacts"
						class="tab-pane fade"
						role="tabpanel"
						aria-labelledby="profile-tab"
					>
						<h2>
							Contacts
						</h2>
						<p class="text-instructions">
							Below are a list of contacts who are connected to this
							organisation.
						</p>
						<customers-list-module
							:customer-results="localCustomerResults"
							@remove_customer="removeCustomer($event)"
						></customers-list-module>

						<!-- ADD CUSTOMER BUTTON -->
						<!-- ADD IN PERMISSIONS -->
						<hr v-if="userLevel > 1"/>
						<div
							v-if="userLevel > 1"
							class="row submit-row"
						>
							<div class="col-md-12">
								<button
									class="btn btn-primary save-changes"
									@click="addNewContact"
								>
									Add Contact
								</button>
							</div>
						</div>
					</div>
					<div
						id="document-uploads"
						class="tab-pane fade"
						role="tabpanel"
						aria-labelledby="profile-tab"
					>
						<documents-module
							:destination="destination"
							:location-id="locationId"
						></documents-module>

						<upload-document-wizard></upload-document-wizard>

						<add-folder-wizard
							:destination="destination"
							:location-id="locationId"
						></add-folder-wizard>

						<add-link-wizard
							:destination="destination"
							:location-id="locationId"
						></add-link-wizard>

						<confirm-file-delete-vue></confirm-file-delete-vue>
					</div>
					<div
						id="associated-objects"
						class="tab-pane fade"
						role="tabpanel"
						aria-labelledby="profile-tab"
					>
						<associated-objects
						></associated-objects>
					</div>
					<div
						id="misc-modules"
						class="tab-pane fade"
						role="tabpanel"
						aria-labelledby="profile-tab"
					>
						<list-tags-module></list-tags-module>
					</div>
					<div
						id="notes-modules"
						class="tab-pane fade"
						role="tabpanel"
						aria-labelledby="profile-tab"
					>
						<notes-module
							:location-id="locationId"
							:destination="destination"
						></notes-module>

						<edit-history-note-wizard></edit-history-note-wizard>

						<new-history-note-wizard
							:location-id="locationId"
							:destination="destination"
						></new-history-note-wizard>

						<confirm-note-delete></confirm-note-delete>
					</div>

					<div
						v-if="userLevel === 4"
						id="admin"
						class="tab-pane fade bg-danger"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
						<delete-object></delete-object>
					</div>
				</div>
			</div>

			<!-- MODALS -->
			<new-customer-modal
				:organisation-id="locationId"
				:title-list="titleList"
			></new-customer-modal>

			<add-tag-wizard></add-tag-wizard>
		</div>
	</n-config-provider>
</template>

<script>
import {Modal} from "bootstrap";

//Components
import CustomersListModule from "Modules/sub_modules/CustomersListModule.vue";
import ListTagsModule from "Modules/sub_modules/ListTagsModule.vue";
import NewCustomerModal from "Components/customers/NewCustomerModal.vue";
import NotesModule from "Modules/sub_modules/NotesModule.vue";
import AssociatedObjects from "Modules/sub_modules/AssociatedObjects.vue";
import DocumentsModule from "Modules/sub_modules/DocumentsModule.vue";
import ConfirmFileDeleteVue from "Modules/wizards/ConfirmFileDelete.vue";
import UploadDocumentWizard from "Modules/wizards/UploadDocumentWizard.vue";
import AddLinkWizard from "Modules/wizards/AddLinkWizard.vue";
import AddFolderWizard from "Modules/wizards/AddFolderWizard.vue";
import EditHistoryNoteWizard from "Modules/wizards/EditHistoryNoteWizard.vue";
import NewHistoryNoteWizard from "Modules/wizards/NewHistoryNoteWizard.vue";
import ConfirmNoteDelete from "Modules/wizards/ConfirmNoteDelete.vue";
import AddTagWizard from "Modules/wizards/AddTagWizard.vue";
import DeleteObject from "Modules/sub_modules/DeleteObject.vue";

//Composables
import {useNBTheme} from "Composables/theme/useNBTheme";

export default {
	name: "OrganisationModules",
	components: {
		AddTagWizard,
		AddFolderWizard,
		AddLinkWizard,
		AssociatedObjects,
		ConfirmFileDeleteVue,
		ConfirmNoteDelete,
		CustomersListModule,
		DeleteObject,
		DocumentsModule,
		EditHistoryNoteWizard,
		ListTagsModule,
		NewCustomerModal,
		NewHistoryNoteWizard,
		NotesModule,
		UploadDocumentWizard,
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
		userExtraPermissions: {
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
	emits: ["remove_customer"],
	data() {
		return {
			localCustomerResults: this.customerResults,
		}
	},
	computed: {
		// ...mapGetters({
		//     userLevel: 'getUserLevel',
		// }),
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
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
		});

		this.$store.commit({
			type: "updateUserExtraPermissions",
			userExtraPermissions: this.userExtraPermissions,
		});
	},
	methods: {
		useNBTheme,
		addNewContact() {
			const new_customer_modal = new Modal(
				document.getElementById("addCustomerModal")
			);
			new_customer_modal.show();
		},
		removeCustomer(customer_id) {
			this.localCustomerResults = this.localCustomerResults.filter((row) => {
				return parseInt(row.pk) !== parseInt(customer_id);
			});
		},
	},
};
</script>



<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<ul
					class="nav nav-tabs"
					id="misc_module_tabs"
					role="tablist"
				>
					<!-- GROUPS AND USERS -->
					<!-- Don't need to show to requirement items - as permissions are gained from parent requirement -->
					<li
						class="nav-item"
						role="presentation"
						v-if="destination !== 'requirement_item'"
					>
						<button
							class="nav-link active"
							id="group-and-user-tab"
							data-bs-toggle="tab"
							data-bs-target="#group-and-users"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Groups and Users
						</button>
					</li>

					<!-- REQUIREMENT ITEMS -->
					<li
						class="nav-item"
						role="presentation"
						v-if="destination === 'requirement'"
					>
						<button
							class="nav-link"
							id="requirement-item-tab"
							data-bs-toggle="tab"
							data-bs-target="#requirement-items"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="false"
						>
							Requirement Item
						</button>
					</li>

					<!-- REQUIREMENT LINKS -->
					<li
						class="nav-item"
						role="presentation"
						v-if="destination === 'requirement'"
					>
						<button
							class="nav-link"
							id="requirement-link-tab"
							data-bs-toggle="tab"
							data-bs-target="#requirement-links"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="false"
						>
							Requirement Links
						</button>
					</li>

					<!-- REQUIREMENT ITEM LINKS -->
					<li
						class="nav-item"
						role="presentation"
						v-if="destination === 'requirement_item'"
					>
						<button
							class="nav-link"
							id="requirement-item-link-tab"
							data-bs-toggle="tab"
							data-bs-target="#requirement-item-links"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="false"
						>
							Links
						</button>
					</li>

					<!-- DOCUMENTS -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link"
							id="documents-tab"
							data-bs-toggle="tab"
							data-bs-target="#documents"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="false"
						>
							Documents
						</button>
					</li>

					<!-- LINKED OBJECTS -->
					<li
						class="nav-item"
						role="presentation"
						v-if="
						destination !== 'requirement' &&
						destination !== 'requirement_item'
					"
					>
						<button
							class="nav-link"
							id="object-link-tabs"
							data-bs-toggle="tab"
							data-bs-target="#object-links"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="false"
						>
							Linked Objects
						</button>
					</li>

					<!-- CUSTOMERS -->
					<!-- Customers are not needed by requirement items as the parent requirements take care of this -->
					<li
						class="nav-item"
						role="presentation"
						v-if="destination !== 'requirement_item'"
					>
						<button
							class="nav-link"
							id="customer-tab"
							data-bs-toggle="tab"
							data-bs-target="#customers"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="false"
						>
							Customers
						</button>
					</li>

					<!-- SPRINTS -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link"
							id="sprints-tab"
							data-bs-toggle="tab"
							data-bs-target="#sprints"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="false"
						>
							Sprints
						</button>
					</li>

					<!-- MISC -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link"
							id="misc-tab"
							data-bs-toggle="tab"
							data-bs-target="#misc"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="false"
						>
							Misc
						</button>
					</li>

					<!-- Notes -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link"
							id="notes-tab"
							data-bs-toggle="tab"
							data-bs-target="#notes"
							type="button"
							role="tab"
							aria-controls="home"
							aria-select="false"
						>
							Notes
						</button>
					</li>
				</ul>
				<hr/>

				<div
					class="tab-content"
					id="misc_module_content"
				>
					<div
						v-if="destination !== 'requirement_item'"
						class="tab-pane fade show active"
						id="group-and-users"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
						<groups-and-users-module></groups-and-users-module>
					</div>
					<div
						class="tab-pane fade"
						id="requirement-items"
						role="tabpanel"
						aria-labelledby="home-tab"
						v-if="destination === 'requirement'"
					>
						<requirement-items-module></requirement-items-module>
					</div>
					<div
						class="tab-pane fade"
						id="requirement-links"
						role="tabpanel"
						aria-labelledby="profile-tab"
						v-if="destination === 'requirement'"
					>
						<requirement-links-module></requirement-links-module>
					</div>
					<div
						class="tab-pane fade"
						id="requirement-item-links"
						role="tabpanel"
						aria-labelledby="profile-tab"
						v-else-if="destination === 'requirement_item'"
					>
						<requirement-item-links-module></requirement-item-links-module>
					</div>

					<div
						class="tab-pane fade"
						id="documents"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
						<documents-module></documents-module>

						<upload-document-wizard></upload-document-wizard>

						<add-folder-wizard
							v-bind:destination="destination"
							v-bind:location-id="locationId"
						></add-folder-wizard>

						<add-link-wizard
							v-bind:destination="destination"
							v-bind:location-id="locationId"
						></add-link-wizard>

						<confirm-file-delete-vue></confirm-file-delete-vue>
						<confirm-folder-delete></confirm-folder-delete>
					</div>
					<div
						class="tab-pane fade"
						id="object-links"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
						<object-links></object-links>
					</div>
					<div
						class="tab-pane fade"
						id="customers"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
						<customers-module></customers-module>
					</div>
					<div
						class="tab-pane fade"
						id="sprints"
						role="tabpanel"
						aria-labelledby="tabpanel"
					>
						<list-sprints></list-sprints>
					</div>
					<div
						class="tab-pane fade"
						id="misc"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
						<misc-module></misc-module>
					</div>
					<div
						class="tab-pane fade"
						id="notes"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
						<notes-module></notes-module>

						<!-- Modals for Notes section -->
						<edit-history-note-wizard></edit-history-note-wizard>

						<new-history-note-wizard
							v-bind:location-id="locationId"
							v-bind:destination="destination"
						></new-history-note-wizard>

						<confirm-note-delete></confirm-note-delete>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import GroupsAndUsersModule from "./sub_modules/GroupsAndUsersModule.vue";
import RequirementItemsModule from "./sub_modules/RequirementItemsModule.vue";
import RequirementItemLinksModule from "./sub_modules/RequirementItemLinksModule.vue";
import RequirementLinksModule from "./sub_modules/RequirementLinksModule.vue";
import DocumentsModule from "./sub_modules/DocumentsModule.vue";
import ObjectLinks from "./sub_modules/ObjectLinks.vue";
import CustomersModule from "./sub_modules/CustomersModule.vue";
import MiscModule from "./sub_modules/MiscModule.vue";
import NotesModule from "./sub_modules/NotesModule.vue";
import UploadDocumentWizard from "./wizards/UploadDocumentWizard.vue";
import AddLinkWizard from "./wizards/AddLinkWizard.vue";
import ConfirmFileDeleteVue from "./wizards/ConfirmFileDelete.vue";
import ConfirmFolderDelete from "./wizards/ConfirmFolderDelete.vue";
import AddFolderWizard from "./wizards/AddFolderWizard.vue";
import ListSprints from "./sub_modules/ListSprints.vue";
import EditHistoryNoteWizard from "./wizards/EditHistoryNoteWizard.vue";
import NewHistoryNoteWizard from "./wizards/NewHistoryNoteWizard.vue";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import ConfirmNoteDelete from "./wizards/ConfirmNoteDelete.vue";

export default {
	name: "ParentModules",
	components: {
		ConfirmNoteDelete,
		AddFolderWizard,
		ConfirmFileDeleteVue,
		AddLinkWizard,
		ConfirmFolderDelete,
		CustomersModule,
		DocumentsModule,
		EditHistoryNoteWizard,
		GroupsAndUsersModule,
		ListSprints,
		NewHistoryNoteWizard,
		NotesModule,
		ObjectLinks,
		RequirementItemLinksModule,
		RequirementItemsModule,
		RequirementLinksModule,
		UploadDocumentWizard,
		MiscModule,
	},
	mixins: [
		getThemeMixin
	],
	props: {
		destination: {
			type: String,
			default: "",
		}, //Which object we are looking at, i.e. requirement
		isReadOnly: {
			type: Boolean,
			default: false,
		},
		locationId: {
			type: Number,
			default: 0,
		}, //The ID of the object we are looking at.
		rootUrl: {
			type: String,
			default: "/",
		},
		staticUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
		},
		userLevel: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {};
	},
	methods: {},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		//Send data to required VueX states
		this.$store.commit({
			type: "updateDestination",
			destination: this.destination,
			locationId: this.locationId,
		});
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		//If is read only is true, we drop the user level to 1.
		if (this.isReadOnly) {
			//Set everything as read only :)
			this.$store.commit({
				type: "updateUserLevel",
				userLevel: 1,
			});
		} else {
			//Use the user level
			this.$store.commit({
				type: "updateUserLevel",
				userLevel: this.userLevel,
			});
		}
	},
};
</script>

<style scoped></style>

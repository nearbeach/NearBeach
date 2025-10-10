<template>
	<div
		id="cardInformationModal"
		class="modal fade"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-xl modal-fullscreen-xl-down">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Card Information - {{ cardId }}
					</h2>
					<button
						id="cardInformationModalCloseButton"
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body mt-4">
					<!-- TAB MENU -->
					<ul
						id="card_information_tabs"
						class="nav nav-tabs"
						role="tablist"
					>
						<li
							class="nav-item"
							role="presentation"
						>
							<button
								id="details-tab"
								class="nav-link active"
								data-bs-toggle="tab"
								data-bs-target="#card_details"
								type="button"
								role="tab"
								aria-controls="home"
								aria-selected="true"
							>
								Details
							</button>
						</li>
						<li
							class="nav-item"
							role="presentation"
						>
							<button
								id="description-tab"
								class="nav-link"
								data-bs-toggle="tab"
								data-bs-target="#card_description"
								type="button"
								role="tab"
								aria-controls="profile"
								aria-selected="false"
							>
								Description
							</button>
						</li>
						<li
							class="nav-item"
							role="presentation"
						>
							<button
								id="notes-tab"
								class="nav-link"
								data-bs-toggle="tab"
								data-bs-target="#card_notes"
								type="button"
								role="tab"
								aria-controls="contact"
								aria-selected="false"
							>
								Notes
							</button>
						</li>
						<li
							class="nav-item"
							role="presentation"
						>
							<button
								id="users-tab"
								class="nav-link"
								data-bs-toggle="tab"
								data-bs-target="#user_permissions"
								type="button"
								role="tab"
								aria-controls="contact"
								aria-selected="false"
							>
								Users
							</button>
						</li>
						<li
							class="nav-item"
							role="presentation"
						>
							<button
								id="downloads-tab"
								class="nav-link"
								data-bs-toggle="tab"
								data-bs-target="#downloads"
								type="button"
								role="tab"
								aria-controls="contact"
								aria-selected="false"
							>
								Downloads
							</button>
						</li>
						<li
							class="nav-item"
							role="presentation"
						>
							<button
								id="misc-tab"
								class="nav-link"
								data-bs-toggle="tab"
								data-bs-target="#misc"
								type="button"
								role="tab"
								aria-controls="contact"
								aria-selected="false"
							>
								Misc
							</button>
						</li>
					</ul>
					<hr/>

					<!-- CONTENT OF TABS -->
					<div
						id="myTabContent"
						class="tab-content"
					>
						<div
							id="card_details"
							class="tab-pane fade show active"
							role="tabpanel"
							aria-labelledby="details-tab"
						>
							<card-details
								@update_card="updateCard($event)"
							></card-details>
						</div>

						<div
							id="card_description"
							class="tab-pane fade"
							role="tabpanel"
							aria-labelledby="description-tab"
						>
							<card-description
								@update_card="updateCard($event)"
							></card-description>
						</div>

						<div
							id="card_notes"
							class="tab-pane fade"
							role="tabpanel"
							aria-labelledby="notes-tab"
						>
							<card-notes></card-notes>
						</div>

						<div
							id="user_permissions"
							class="tab-pane fade"
							role="tabpanel"
							aria-labelledby="user-tab"
						>
							<card-users></card-users>
						</div>
						<div
							id="downloads"
							class="tab-pane fade"
							role="tabpanel"
							aria-labelledby="user-tab"
						>
							<documents-module
								override-destination="kanban_card"
								:override-location-id="cardId"
								:read-only="kanbanStatus === 'Closed'"
							></documents-module>
						</div>
						<div
							id="misc"
							class="tab-pane fade"
							role="tabpanel"
							aria-labelledby="user-tab"
						>
							<list-tags-module
override-destination="kanban_card"
											  close-modal-before="cardInformationModalCloseButton"
											  :override-location-id="cardId"
							></list-tags-module>

							<list-public-links
override-destination="kanban_card"
											   :override-location-id="cardId"
											   :is-read-only="kanbanStatus === 'Closed'"
							></list-public-links>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import CardDetails from "./CardDetails.vue";
import CardNotes from "./CardNotes.vue";
import CardDescription from "./CardDescription.vue";
import CardUsers from "./CardUsers.vue";
import DocumentsModule from 'Modules/sub_modules/DocumentsModule.vue';
import ListPublicLinks from "Modules/sub_modules/ListPublicLinks.vue";

//VueX
import {mapGetters} from "vuex";

import ListTagsModule from "Modules/sub_modules/ListTagsModule.vue";

export default {
	name: "CardInformation",
	components: {
		ListTagsModule,
		CardDescription,
		CardDetails,
		CardNotes,
		CardUsers,
		DocumentsModule,
		ListPublicLinks,
	},
	emits: [
		'update_card',
	],
	data() {
		return {
			cardDescriptionModel: "",
			cardNoteModel: "",
			cardTitleModel: "",
			noteHistoryResults: [],
		};
	},
	computed: {
		...mapGetters({
			cardId: "getCardId",
			kanbanStatus: "getKanbanStatus",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		updateCard(data) {
			//Notify the user we are updating the card
			this.$store.dispatch("newToast", {
				header: "Updating Current Card",
				message: "Please wait - we are updating the card's information",
				extra_classes: "bg-warning text-dark",
				unique_type: "update-card",
				delay: 0,
			});

			//Get all data from VueX
			const all_data = this.$store.getters.getAllCardData;

			//Setup data_to_send
			const data_to_send = new FormData();
			data_to_send.set("kanban_card_text", all_data.cardTitle);
			data_to_send.set(
				"kanban_card_description",
				all_data.cardDescription
			);
			data_to_send.set("kanban_level", all_data.cardLevel);
			data_to_send.set("kanban_column", all_data.cardColumn);
			data_to_send.set("kanban_card_id", all_data.cardId);
			data_to_send.set("kanban_card_priority", all_data.cardPriority);

			//If there is new_destination or old_destination, we want to send that data into the backend too
			if (data.new_destination !== undefined) {
				data.new_destination.forEach((row) => {
					data_to_send.append("new_destination", row.kanban_card_id);
				});
			}

			if (data.old_destination !== undefined) {
				data.old_destination.forEach((row) => {
					data_to_send.append("old_destination", row.kanban_card_id);
				});
			}

			//Use Axios to send data to backend
			this.axios.post(
				`${this.rootUrl}kanban_information/update_card/`,
				data_to_send
			).then(() => {
				//Send the new data upstream
				this.$emit("update_card", {
					kanban_card_id: all_data.cardId,
					kanban_card_text: all_data.cardTitle,
					kanban_card_description:
					all_data.cardDescription,
					// kanban_column: all_data.cardColumn,
					// kanban_level: all_data.cardLevel,
					// kanban_card_priority: all_data.cardPriority,
				});

				//Notify user of successful update
				this.$store.dispatch("newToast", {
					header: "Card successfully updated",
					message: "Your card has successfully update",
					extra_classes: "bg-success",
					unique_type: "update-card",
				});

				//Only close if data.close_modal is true
				if (data.close_modal) {
					document
						.getElementById("cardInformationModalCloseButton")
						.click();
				}
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Card failed to updated",
					message: `Sorry your card failed to update - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "update-card",
				});
			});
		},
	},
};
</script>



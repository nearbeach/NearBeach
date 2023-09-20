<template>
	<div
		class="modal fade"
		id="cardInformationModal"
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
						<Icon v-bind:icon="icons.usersIcon"></Icon>
						Card
						Information - {{ cardId }}
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="cardInformationModalCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
					<br/>
				</div>
				<div class="modal-body">
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
								class="nav-link active"
								id="details-tab"
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
								class="nav-link"
								id="description-tab"
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
								class="nav-link"
								id="notes-tab"
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
								class="nav-link"
								id="users-tab"
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
								class="nav-link"
								id="downloads-tab"
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
					</ul>
					<hr/>

					<!-- CONTENT OF TABS -->
					<div
						class="tab-content"
						id="myTabContent"
					>
						<div
							class="tab-pane fade show active"
							id="card_details"
							role="tabpanel"
							aria-labelledby="details-tab"
						>
							<card-details
								v-on:update_card="updateCard($event)"
							></card-details>
						</div>

						<div
							class="tab-pane fade"
							id="card_description"
							role="tabpanel"
							aria-labelledby="description-tab"
						>
							<card-description
								v-on:update_card="updateCard($event)"
							></card-description>
						</div>

						<div
							class="tab-pane fade"
							id="card_notes"
							role="tabpanel"
							aria-labelledby="notes-tab"
						>
							<card-notes></card-notes>
						</div>

						<div
							class="tab-pane fade"
							id="user_permissions"
							role="tabpanel"
							aria-labelledby="user-tab"
						>
							<card-users></card-users>
						</div>
						<div
							class="tab-pane fade"
							id="downloads"
							role="tabpanel"
							aria-labelledby="user-tab"
						>
							<documents-module
								v-bind:override-destination="'kanban_card'"
								v-bind:override-location-id="cardId"
							></documents-module>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";
import {Icon} from "@iconify/vue";
import CardDetails from "./CardDetails.vue";
import CardNotes from "./CardNotes.vue";
import CardDescription from "./CardDescription.vue";
import CardUsers from "./CardUsers.vue";
import DocumentsModule from '../modules/sub_modules/DocumentsModule.vue';

//VueX
import {mapGetters} from "vuex";

//Mixins
import iconMixin from "../../mixins/iconMixin";

export default {
	name: "CardInformation",
	components: {
		CardDescription,
		CardDetails,
		CardNotes,
		CardUsers,
		DocumentsModule,
		Icon,
	},
	mixins: [iconMixin],
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
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		updateCard(data) {
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

			//Use Axios to send data to backend
			axios
				.post(
					`${this.rootUrl}kanban_information/update_card/`,
					data_to_send
				)
				.then(() => {
					//Send the new data upstream
					this.$emit("update_card", {
						kanban_card_id: all_data.cardId,
						kanban_card_text: all_data.cardTitle,
						kanban_card_description:
						all_data.cardDescriptionModel,
						kanban_column: all_data.cardColumn,
						kanban_level: all_data.cardLevel,
						kanban_card_priority: all_data.cardPriority,
					});

					//Only close if data.close_modal is true
					if (data.close_modal) {
						document
							.getElementById("cardInformationModalCloseButton")
							.click();
					}
				})
				.catch((error) => {
				});
		},
	},
};
</script>

<style scoped></style>

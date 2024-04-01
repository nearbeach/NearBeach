<template>
	<n-config-provider :theme="getTheme(theme)">
		<div>
			<h1 class="kanban-header">
				{{ kanbanBoardResults[0].fields.kanban_board_name }}
			</h1>
			<div class="btn-group kanban-menu"
				v-if="userLevel >= 2"
			>
				<button class="btn btn-secondary btn-sm dropdown-toggle"
						type="button"
						data-bs-toggle="dropdown"
						aria-expanded="false"
				>
					Kanban Menu
				</button>
				<ul class="dropdown-menu">
					<li><a class="dropdown-item" href="#">
						<n-switch v-model:value="canDragCards"
								  @update:value="updateCanDragCards"
								  v-if="kanbanBoardResults[0].fields.kanban_board_status !== 'Closed' && userLevel >= 2"
						>
							<template #checked>
								Can Drag Cards
							</template>
							<template #unchecked>
								Card Position Locked
							</template>
						</n-switch>
					</a></li>
					<li>
						<hr class="dropdown-divider"
							v-if="userLevel >= 3"
						>
					</li>
					<li><a
						class="dropdown-item"
						href="#"
						v-on:click="addNewKanbanCard()"
					>
						Add New Card
					</a></li>
					<li><a
						class="dropdown-item"
						href="#"
						v-on:click="addNewLink()"
					>
						Add New Link to Object
					</a></li>
					<li>
						<hr class="dropdown-divider"
							v-if="userLevel >= 3"
						>
					</li>
					<li>
						<a
							class="dropdown-item"
							v-bind:href="`${rootUrl}kanban_information/${kanbanBoardResults[0].pk}/edit_board/`"
						   	v-if="userLevel >= 3"
						>
							Edit Kanban
						</a>
					</li>
				</ul>
			</div>

			<div v-if="userLevel <= 1"
				 style="height: 31px; width: 100%;"
			></div>

			<!-- Rendering the Kanban Container -->
			<kanban-board
				v-bind:kanban-board-results="kanbanBoardResults"
				v-bind:new-card-info="newCardInfo"
				v-on:double_clicked_card="doubleClickedCard($event)"
			></kanban-board>

			<!-- MODALS -->
			<add-user-to-card
				v-bind:destination="'kanban_card'"
				v-bind:location-id="cardId"
				v-bind:refresh-user-list="refreshUserList"
				v-on:reset_refresh_user_list="resetRefreshUserList"
			></add-user-to-card>

			<archive-cards></archive-cards>

			<blocked-notes-modal></blocked-notes-modal>

			<confirm-card-archive
				v-bind:card-information="cardInformation"
			></confirm-card-archive>

			<new-kanban-card
				v-bind:kanban-card-results="kanbanCardResults"
				v-bind:column-results="columnResults"
				v-bind:level-results="levelResults"
				v-bind:kanban-board-results="kanbanBoardResults"
				v-on:new_card="newCard($event)"
			></new-kanban-card>

			<card-information
				v-bind:card-information="cardInformation"
				v-on:update_card="updateCard($event)"
			></card-information>

			<upload-document-wizard
				v-bind:override-destination="'kanban_card'"
				v-bind:override-location-id="cardId"
			></upload-document-wizard>

			<edit-history-note-wizard></edit-history-note-wizard>

			<new-history-note-wizard
				v-bind:location-id="cardId"
				v-bind:destination="'kanban_card'"
			></new-history-note-wizard>

			<confirm-note-delete></confirm-note-delete>

			<add-folder-wizard
				v-bind:destination="'kanban_card'"
				v-bind:location-id="locationId"
			></add-folder-wizard>

			<add-link-wizard
				v-bind:destination="'kanban_card'"
				v-bind:location-id="locationId"
			></add-link-wizard>

			<!-- CONFIRM DOCUMENT DELETE -->
			<confirm-file-delete-vue></confirm-file-delete-vue>
			<confirm-folder-delete></confirm-folder-delete>

			<new-kanban-link-wizard
				v-bind:location-id="locationId"
				v-bind:column-results="columnResults"
				v-bind:level-results="levelResults"
				v-on:new_card="newCard($event)"
			></new-kanban-link-wizard>
		</div>
	</n-config-provider>
</template>

<script>
import AddUserToCard from "../card_information/AddUserToCard.vue";
import ArchiveCards from "./ArchiveCards.vue";
import BlockedNotesModal from "./BlockedNotesModal.vue";
import KanbanBoard from "./KanbanBoard.vue";
import NewKanbanCard from "../modules/wizards/NewKanbanCard.vue";
import CardInformation from "../card_information/CardInformation.vue";
import NewKanbanLinkWizard from "../modules/wizards/NewKanbanLinkWizard.vue";
import ConfirmCardArchive from "./ConfirmCardArchive.vue";

//VueX
import {mapGetters} from "vuex";

//Naive UI
import {NSwitch} from "naive-ui";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import UploadDocumentWizard from "../modules/wizards/UploadDocumentWizard.vue";
import AddFolderWizard from "../modules/wizards/AddFolderWizard.vue";
import AddLinkWizard from "../modules/wizards/AddLinkWizard.vue";
import ConfirmFileDeleteVue from "../modules/wizards/ConfirmFileDelete.vue";
import ConfirmFolderDelete from "../modules/wizards/ConfirmFolderDelete.vue";
import EditHistoryNoteWizard from "../modules/wizards/EditHistoryNoteWizard.vue";
import NewHistoryNoteWizard from "../modules/wizards/NewHistoryNoteWizard.vue";
import ConfirmNoteDelete from "../modules/wizards/ConfirmNoteDelete.vue";
import {Modal} from "bootstrap";

export default {
	name: "KanbanInformation",
	components: {
		ConfirmNoteDelete,
		NewHistoryNoteWizard,
		EditHistoryNoteWizard,
		ConfirmFolderDelete,
		ConfirmFileDeleteVue,
		AddLinkWizard,
		AddFolderWizard,
		UploadDocumentWizard,
		AddUserToCard,
		ArchiveCards,
		BlockedNotesModal,
		CardInformation,
		ConfirmCardArchive,
		KanbanBoard,
		NewKanbanCard,
		NewKanbanLinkWizard,
		NSwitch,
	},
	props: {
		columnResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		kanbanBoardResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		kanbanCardResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		kanbanSettings: {
			type: Object,
			default: () => {
				return {
					setting_data: {
						canDragCards: true,
						levels: [],
					},
				};
			},
		},
		levelResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		locationId: {
			type: Number,
			default: 0,
		},
		openCardOnLoad: {
			type: Number,
			default: 0,
		},
		potentialUserList: {
			type: Array,
			default: () => {
				return [];
			},
		},
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
	computed: {
		...mapGetters({
			cardId: "getCardId",
		}),
	},
	watch: {
		cardId() {
			this.refreshUserList = true;
		},
	},
	mixins: [
		getThemeMixin,
	],
	data() {
		return {
			canDragCards: true,
			cardInformation: {},
			localKanbanCardResults: this.kanbanCardResults,
			refreshUserList: false,
			newCardInfo: [],
		};
	},
	methods: {
		addNewKanbanCard() {
			//Update New Card VueX to use this location
			this.$store.commit({
				type: "updateNewCardLocation",
				columnId: this.columnResults[0].pk,
				levelId: this.levelResults[0].pk,
				userCanSelectLocation: true,
			});

			//Get the Modal from the above modal
			const modalInstance = new Modal(document.getElementById("addKanbanCardModal"));
			modalInstance.show();
		},
		addNewLink() {
			//Update New Card VueX to use this location
			this.$store.commit({
				type: "updateNewCardLocation",
				columnId: this.columnResults[0].pk,
				levelId: this.levelResults[0].pk,
				userCanSelectLocation: true,
			});

			//Get the Modal from the above modal
			const modalInstance = new Modal(document.getElementById("newLinkModal"));
			modalInstance.show();
		},
		doubleClickedCard(data) {
			//Update the cardInformationId with the card id
			this.cardInformation = data;
		},
		newCard(data) {
			//this.newCardInfo = data;

			this.$store.commit({
				type: "addCard",
				newCard: data,
			});
		},
		resetRefreshUserList() {
			this.refreshUserList = false;
		},
		updateCanDragCards(value) {
			// this.$store.commit({
			// 	type: "updateCanDragCards",
			// 	canDragCards: value,
			// })
			this.$store.dispatch({
				type: "updateCanDragCards",
				canDragCards: value,
			});
		},
		updateCard(data) {
			//Loop through the results - when the id's match. Update the data.
			this.localKanbanCardResults.forEach((row, index) => {
				//Check to see if the primary keys match - if they do update the data
				if (row.pk === data.kanban_card_id) {
					this.localKanbanCardResults[
						index
						].fields.kanban_card_text = data.kanban_card_text;
					this.localKanbanCardResults[
						index
						].fields.kanban_card_description =
						data.kanban_card_description;
					// this.localKanbanCardResults[
					// 	index
					// 	].fields.kanban_column = data.kanban_column;
					// this.localKanbanCardResults[index].fields.kanban_level =
					// 	data.kanban_level;
					// this.localKanbanCardResults[index].fields.kanban_card_priority =
					// 	data.kanban_card_priority;
				}
			});
		},
		updateKanbanSettings() {
			//If there are no settings - just return
			if (this.kanbanSettings.setting_data === undefined) return;

			//Setup the canDrag
			let can_drag_cards = this.kanbanSettings.setting_data.canDragCards;
			if (can_drag_cards === undefined) can_drag_cards = true;

			//Update local
			this.canDragCards = can_drag_cards;

			//Setup the kanban levels collapse
			let levels = this.kanbanSettings.setting_data.levels;
			if (levels === undefined) levels = [];

			//Check to see if we are missing any levels
			const level_id_array = levels.map(row => {
				return row.level_id
			});
			const missing_levels = this.levelResults.filter((row) => {
				//Find those that don't exist in level results
				return level_id_array.indexOf(row.pk) === -1;
			})

			//Loop through the missing levels and add them to levels
			missing_levels.forEach((row) => {
				levels.push({
					level_id: row.pk,
					is_collapsed: false,
				});
			});

			//Remove any levels that no longer exist
			const all_levels_array = this.levelResults.map((row) => {
				return row.pk;
			});
			levels = levels.filter((row) => {
				return all_levels_array.indexOf(row.level_id) >= 0;
			})


			//Data is ready to upload
			this.$store.commit({
				type: "initKanbanSettings",
				canDragCards: can_drag_cards,
				levels: levels,
			})
		}
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		//Send the settings up stream
		this.updateKanbanSettings();

		//Send data to VueX
		this.$store.commit({
			type: "initPayload",
			kanbanCardResults: this.kanbanCardResults,
			levelResults: this.levelResults,
			columnResults: this.columnResults,
			openCardOnLoad: this.openCardOnLoad,
		});

		//Send the urls upstream
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		this.$store.commit({
			type: "updateDestination",
			destination: "kanban_board",
			locationId: this.locationId,
		});

		//Send columns and levels into the VueX
		this.$store.commit({
			type: "updateLists",
			columnResults: this.columnResults,
			levelResults: this.levelResults,
		});

		//Update the user permissions
		this.$store.commit({
			type: "updateUserLevel",
			userLevel: this.userLevel,
		});

		//Update groups and users
		this.$store.commit({
			type: "updateGroupsAndUsers",
			potentialUserList: this.potentialUserList,
		})
	},
};
</script>

<style scoped></style>

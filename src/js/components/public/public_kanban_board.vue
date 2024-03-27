<template>
	<n-config-provider :theme="getTheme(theme)">
			<h1 class="kanban-header">
				{{ kanbanBoardResults[0].fields.kanban_board_name }}
			</h1>
			<br/>

			<div id="kanban_container"
				 class="kanban-container"
				 v-on:scroll="scrollProcedure"
			>
				<!-- Render out the header -->
				<div class="kanban-header-row">
					<div
						class="kanban-column-header"
						v-for="column in columnResults"
						:key="column.pk"
					>
						{{ column.fields.kanban_column_name }}
					</div>
				</div>

				<!-- Render out the STICKY header -->
				<div
					class="kanban-header-row kanban-sticky-row"
					style="display: none"
				>
					<div
						class="kanban-column-header"
						v-for="column in columnResults"
						:key="column.pk"
					>
						{{ column.fields.kanban_column_name }}
					</div>
				</div>

				<!-- Render each row -->
				<div
					v-for="level in levelResults"
					:key="level.pk"
				>
					<!-- CREATE THE LEVEL HEADER -->
					<div class="kanban-level-div">
						{{ level.fields.kanban_level_name }}
					</div>

					<div class="kanban-row">
						<public-kanban-column
							v-for="column in columnResults"
							:key="column.pk"
							v-bind:master-list="filterCards(column.pk, level.pk)"
							v-on:card_clicked="cardClicked($event)"
						></public-kanban-column>
					</div>
				</div>
			</div>
	</n-config-provider>

	<!-- Modal -->
	<div class="modal fade modal-xl" id="kanbanCardModal" tabindex="-1" role="dialog" aria-labelledby="kanbanCardModalTitle" aria-hidden="true">
		<div class="modal-dialog modal-dialog-centered" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="kanbanCardModalHeader"
					>
						Kanban Card {{cardId}}
					</h5>
					<button
						type="button"
						class="btn-close"
						aria-label="Close"
						data-bs-dismiss="modal"
					></button>
				</div>
				<div class="modal-body">
					<public-card-information
						v-bind:card-column="cardColumn"
						v-bind:card-id="cardId"
						v-bind:card-description="cardDescription"
						v-bind:card-level="cardLevel"
						v-bind:card-priority="cardPriority"
						v-bind:card-text="cardText"
						v-bind:theme="`light`"
						v-bind:user-level="1"
					></public-card-information>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { NConfigProvider } from "naive-ui";
import PublicKanbanColumn from "./public_kanban_column.vue"
import PublicCardInformation from "./public_card_information.vue"

import { Modal } from "bootstrap";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import KanbanRow from "../kanban/KanbanRow.vue";
export default {
	name: "PublicKanbanBoard",
	components: {
		KanbanRow,
		NConfigProvider,
		PublicCardInformation,
		PublicKanbanColumn,
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
		levelResults: {
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
	data: () => ({
		cardColumn: "",
		cardId: "0",
		cardDescription: "",
		cardLevel: "",
		cardPriority: "",
		cardText: "",
		listPriority: [
			{
				label: "Highest",
				value: 0,
			},
			{
				label: "High",
				value: 1,
			},
			{
				label: "Normal",
				value: 2,
			},
			{
				label: "Low",
				value: 3,
			},
			{
				label: "Lowest",
				value: 4,
			},
		],
	}),
	mixins: [
		getThemeMixin,
	],
	created() {
		window.addEventListener("resize", this.resizeProcedure);
		window.addEventListener("scroll", this.scrollProcedure);
	},
	unmounted() {
		window.removeEventListener("resize", this.resizeProcedure);
		window.removeEventListener("scroll", this.scrollProcedure);
	},
	methods: {
		cardClicked(card_id) {
			//Filter for the card we want
			let card_results = this.kanbanCardResults.filter((row) => {
				return parseInt(row.pk) === parseInt(card_id);
			});

			//If there is no data - don't continue
			if (card_results.length === 0) return;

			//Grab the first result
			card_results = card_results[0];

			this.cardColumn = this.getColumn(card_results.fields.kanban_column);
			this.cardId = `${card_id}`;
			this.cardDescription = card_results.fields.kanban_card_description;
			this.cardLevel = this.getLevel(card_results.fields.kanban_level);
			this.cardPriority = this.getPriorty(card_results.fields.kanban_card_priority);
			this.cardText = `${card_results.fields.kanban_card_text}`;

			//Open the modal
			const modal = new Modal(
				document.getElementById("kanbanCardModal")
			);
			modal.show();
		},
		getColumn(column_id) {
			const column_results = this.columnResults.filter((row) => {
				return parseInt(row.pk) === parseInt(column_id);
			})

			if (column_results.length === 0) return "Unknown";

			return column_results[0].fields.kanban_column_name;
		},
		getLevel(level_id) {
			const level_results = this.levelResults.filter((row) => {
				return parseInt(row.pk) === parseInt(level_id);
			})

			if (level_results.length === 0) return "Unknown";

			return level_results[0].fields.kanban_level_name;
		},
		getPriorty(priority_id) {
			const priority = this.listPriority.filter((row) => {
				return parseInt(row.value) === parseInt(priority_id);
			});

			if (priority.length === 0 ) return "Unknown";

			return priority[0].label;
		},
		filterCards(column_id, level_id) {
			return this.kanbanCardResults.filter((row) => {
				const condition_1 = parseInt(row.fields.kanban_column) === parseInt(column_id);
				const condition_2 = parseInt(row.fields.kanban_level) === parseInt(level_id);

				return condition_1 && condition_2;
			});
		},
		resizeProcedure() {
			// Get the screen size and the columns width
			const little_adjustment = 2 * (this.columnResults.length - 1)
			const columns_width = this.columnResults.length * 400 + little_adjustment;
			const container_element = document.getElementsByClassName("kanban-container")[0];

			//If container element does not exist just return
			if (container_element === undefined) return;

			//Get the kanban container width
			const kanban_container_width = container_element.clientWidth;

			//If the columns width is smaller than the screen size
			// - we will need to adjust the kanban-level-div to match
			// that smaller size
			if (columns_width < kanban_container_width) {
				//Add in the width restrictions
				const header_element = document.getElementsByClassName("kanban-edit-text")[0];
				const elements = document.getElementsByClassName("kanban-level-div");

				//Loop through each element
				Array.from(elements).forEach((element) => {
					element.style = `max-width: ${columns_width}px;`;
				});

				//Adjust the size of the header element
				header_element.style = `max-width: ${columns_width}px`;
			} else {
				//The columns width is greater than the container width.
				//So we need to use the scroll width of the container
				const scroll_width = container_element.scrollWidth;
				const header_element = document.getElementsByClassName("kanban-edit-text")[0];
				let elements = document.getElementsByClassName("kanban-level-div");

				//Loop through each element
				Array.from(elements).forEach((element) => {
					element.style = `width: ${scroll_width}px;`;
				});

				//Adjust the size of the header element
				header_element.style = `max-width: ${scroll_width}px`;
			}
		},
		scrollProcedure() {
			//Make sure the kanban-sticky-row matches the scroll left for the kanban-container
			const kanban_sticky =
					document.getElementsByClassName("kanban-sticky-row")[0],
				kanban_container =
					document.getElementsByClassName("kanban-container")[0];

			kanban_sticky.scrollLeft = kanban_container.scrollLeft;

			//Get the distance to the top of the page
			const scrollTop = document.getElementById("kanban_container").scrollTop;

			//Determine if we are hidding the element or not
			if (scrollTop < 90) {
				kanban_sticky.style.display = "none";
			} else {
				kanban_sticky.style.display = "";
			}
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.resizeProcedure();
		});
	},
}
</script>
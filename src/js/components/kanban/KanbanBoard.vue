<template>
	<div
		id="kanban_container"
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
        		<span v-bind:class="getExpandClass(level.pk)"
					  v-on:click="expandLevel(level.pk)"
				></span>
				<span>
					{{ level.fields.kanban_level_name }}
					- [{{levelCardCount(level.pk)}}]
				</span>
			</div>

			<!-- RENDER THE CELLS -->
			<kanban-row
				v-bind:level-id="level.pk"
				v-bind:new-card-info="newCardInfo"
				v-on:double_clicked_card="doubleClickedCard($event)"
			></kanban-row>
		</div>
	</div>
</template>

<script>
//Mixins
import iconMixin from "../../mixins/iconMixin";
import KanbanRow from "./KanbanRow.vue";

//VueX
import {mapGetters} from "vuex";
import {nextTick} from 'vue';

export default {
	name: "KanbanBoard",
	components: {
		KanbanRow,
	},
	props: {
		kanbanBoardResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		newCardInfo: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	computed: {
		...mapGetters({
			columnResults: "getColumnResults",
			levelCardCount: "getLevelCardCount",
			levelResults: "getLevelResults",
		}),
	},
	mixins: [iconMixin],
	data() {
		return {};
	},
	created() {
		window.addEventListener("resize", this.resizeProcedure);
		window.addEventListener("scroll", this.scrollProcedure);
	},
	unmounted() {
		window.removeEventListener("resize", this.resizeProcedure);
		window.removeEventListener("scroll", this.scrollProcedure);
	},
	methods: {
		doubleClickedCard(data) {
			//Send data upstream
			this.$emit("double_clicked_card", data);
		},
		expandLevel(level_id) {
			//Update the VueX data
			this.$store.dispatch("updateLevelCollapse", {
				level_id: level_id,
			});
		},
		getExpandClass(level_id) {
			//Get the required results from vuex
			const collapsed_status = this.$store.getters.getLevelCollapseStatus(level_id);

			// If getLevel Collasped status is true - it is collapsed
			if (collapsed_status) {
				return "kanban-expand collapsed";
			}

			return "kanban-expand expanded";
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
				// const header_element = document.getElementsByClassName("kanban-edit-text")[0];
				const elements = document.getElementsByClassName("kanban-level-div");

				//Loop through each element
				Array.from(elements).forEach((element) => {
					element.style = `max-width: ${columns_width}px;`;
				});

				//Adjust the size of the header element
				// header_element.style = `max-width: ${columns_width}px`;
			} else {
				//The columns width is greater than the container width.
				//So we need to use the scroll width of the container
				const scroll_width = container_element.scrollWidth;
				// const header_element = document.getElementsByClassName("kanban-edit-text")[0];
				let elements = document.getElementsByClassName("kanban-level-div");

				//Loop through each element
				Array.from(elements).forEach((element) => {
					element.style = `width: ${scroll_width}px;`;
				});

				//Adjust the size of the header element
				// header_element.style = `max-width: ${scroll_width}px`;
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
		//Check the resize procedure
		this.$nextTick(() => {
			this.resizeProcedure();
		});

		this.$store.commit({
			type: "updateKanbanStatus",
			kanbanStatus:
			this.kanbanBoardResults[0].fields.kanban_board_status,
		});
	},
};
</script>

<style scoped></style>

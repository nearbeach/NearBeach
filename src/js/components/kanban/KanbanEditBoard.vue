<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>{{ kanbanBoardResults[0].fields.kanban_board_name }}</h1>
				<hr/>

				<!-- Properties for the drag and drop coloumns/levels -->
				<div class="row">
					<div class="col-md-4">
						<h2>Columns & Levels</h2>
						<p class="text-instructions">
							Drag the cards around to sort out the columns how you
							want them.
						</p>
						<strong>Rename Columns & Levels</strong>
						<p class="text-instructions">
							To rename any level or object, double click on the card.
							This will bring up the card's properties.
						</p>
						<n-switch v-model:value="canDragCards"
								  @update:value="updateCanDragCards"
						>
							<template #checked>
								Can Drag Cards
							</template>
							<template #unchecked>
								Card Position Locked
							</template>
						</n-switch>
					</div>
					<div class="col-md-4">
						<kanban-property-order
							v-bind:is-read-only="isReadOnly"
							v-bind:property-name="'Column'"
							v-bind:property-list="columnModel"
							v-bind:source="'columnModel'"
							v-bind:is-dirty="v$.columnModel.$dirty"
							v-bind:is-new-mode="false"
							v-bind:kanban-board-id="kanbanBoardResults[0].pk"
							v-on:update_property_list="updatePropertyList($event)"
						></kanban-property-order>
					</div>
					<div class="col-md-4">
						<kanban-property-order
							v-bind:is-read-only="isReadOnly"
							v-bind:property-name="'Level'"
							v-bind:property-list="levelModel"
							v-bind:source="'levelModel'"
							v-bind:is-dirty="v$.columnModel.$dirty"
							v-bind:is-new-mode="false"
							v-bind:kanban-board-id="kanbanBoardResults[0].pk"
							v-on:update_property_list="updatePropertyList($event)"
						></kanban-property-order>
					</div>
				</div>

				<!-- SAVE -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button
							class="btn btn-primary save-changes"
							v-on:click="backToBoard"
						>
							Back to Kanban Board
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import {NSwitch} from "naive-ui";

// Components
import KanbanPropertyOrder from "./KanbanPropertyOrder.vue";

// Validation
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";

export default {
	name: "KanbanEditBoard",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		KanbanPropertyOrder,
		NSwitch,
	},
	props: {
		isReadOnly: {
			type: Boolean,
			default: false,
		},
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
	mixins: [getThemeMixin],
	data() {
		return {
			canDragCards: false,
			columnModel: [],
			levelModel: [],
		};
	},
	validations: {
		columnModel: {
			required,
		},
		levelModel: {
			required,
		},
	},
	methods: {
		backToBoard() {
			window.location.href = `${this.rootUrl}kanban_information/${this.kanbanBoardResults[0].pk}/`;
		},
		updateCanDragCards(value) {
			this.$store.commit({
			  type: "updateCanDragCards",
			  canDragCards: value,
			})
			// this.$store.dispatch({
			// 	type: "updateCanDragCards",
			// 	canDragCards: value,
			// });
		},
		updatePropertyList(data) {
			this[data.source] = data.data;
		},
	},
	mounted() {
		//Send the location id and destination
		this.$store.commit({
			type: "updateDestination",
			destination: "kanban_board",
			locationId: this.locationId,
		});

		//Send the rootURL to the vuex
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		this.$store.commit({
			type: "updateUserLevel",
			userLevel: this.userLevel,
		});

		//Map the variables into a useable format
		this.columnModel = this.columnResults.map((row) => {
			return {
				id: row.pk,
				property: row.fields.kanban_column_property,
				title: row.fields.kanban_column_name,
			};
		});

		this.levelModel = this.levelResults.map((row) => {
			return {
				id: row.pk,
				property: "",
				title: row.fields.kanban_level_name,
			};
		});

		//Update Can Drag Cards value
		this.updateCanDragCards(false);
	},
};
</script>

<style scoped></style>

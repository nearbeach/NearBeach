<template>
    <div class="row">
        <div class="col-md-4">
            <h2>Kanban Settings</h2>
            <p class="text-instructions">
                Please search for the kanban board in the dropdown. Then choose the appropriate Kanban Level and Column.
            </p>
        </div>
        <div class="col-md-8">
            <div class="form-group">
                <label for="kanban_board">
                    Kanban Board
                    <validation-rendering
                        v-bind:error-list="v$.kanbanBoardModel.$errors"
                    ></validation-rendering>
                </label>
                <n-select
					:options="kanbanBoardOptions"
					filterable
					placeholder="Search Kanban Boards"
					@search="fetchKanbanBoardOptions"
					v-model:value="kanbanBoardModel"
					label-field="kanban_board_name"
                    value-field="kanban_board_id"
					class="get-stakeholders"
				/>
            </div>
        </div>
    </div>
	<hr />
	<div class="row">
		<div class="col-md-4">
			<h2>Kanban Column/Level</h2>
			<p class="text-instructions">
				Please pick the Column and Level for the Kanban Card.
			</p>
		</div>
		<div class="col-md-4">
			<div class="form-group">
				<label for="kanban_column">
					Kanban Column
					<validation-rendering
						v-bind:error-list="v$.kanbanBoardModel.$errors"
					></validation-rendering>
				</label>
				<n-select
					:options="kanbanColumnOptions"
					filterable
					placeholder="Search Columns"
					v-model:value="kanbanColumnModel"
					label-field="kanban_column_name"
					value-field="kanban_column_id"
				/>
			</div>
		</div>
		<div class="col-md-4">
			<div class="form-group">
				<label for="kanban_board">
					Kanban Level
					<validation-rendering
						v-bind:error-list="v$.kanbanBoardModel.$errors"
					></validation-rendering>
				</label>
				<n-select
					:options="kanbanLevelOptions"
					filterable
					placeholder="Search Levels"
					v-model:value="kanbanLevelModel"
					label-field="kanban_level_name"
					value-field="kanban_level_id"
					class="get-stakeholders"
				/>
			</div>
		</div>
	</div>
</template>

<script>
import {mapGetters} from "vuex";
import ValidationRendering from "Components/validation/ValidationRendering.vue";
import {NSelect} from "naive-ui";
import {required} from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";

export default {
    name: "GetKanbanSettings",
    components: {
        NSelect,
        ValidationRendering
    },
	setup() {
		return {v$: useVuelidate()};
	},
	emits: [
		"update_kanban_settings",
	],
	props: {
		initKanbanBoardId: {
			type: Number,
			default: undefined,
		},
		initKanbanColumnId: {
			type: Number,
			default: undefined,
		},
		initKanbanLevelId: {
			type: Number,
			default: undefined,
		},
	},
    data() {
        return {
            kanbanBoardModel: this.initKanbanBoardId === 0 ? "" : this.initKanbanBoardId,
            kanbanBoardOptions: [],
            kanbanColumnModel: this.initKanbanColumnId === 0 ? "" : this.initKanbanColumnId,
            kanbanColumnOptions: [],
			kanbanLevelModel: this.initKanbanLevelId === 0 ? "" : this.initKanbanLevelId,
			kanbanLevelOptions: [],
        };
    },
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
	},
	validations: {
		kanbanBoardModel: {
			required,
		},
		kanbanLevelModel: {
			required,
		},
		kanbanColumnModel: {
			required,
		},
	},
    watch: {
        kanbanBoardModel() {
			// Clear results
			this.kanbanColumnModel = "";
			this.kanbanLevelModel = "";

            this.fetchKanbanProperties();
			this.updateDetails();
        },
	    kanbanColumnModel() {
			this.updateDetails();
	    },
		kanbanLevelModel() {
			this.updateDetails();
		},
    },
    methods: {
        fetchKanbanBoardOptions() {
            this.axios.get(
                `${this.rootUrl}api/v0/kanban_board/`
            ).then((response) => {
                this.kanbanBoardOptions = response.data.results;

				// If there exists data already, also get the properties
				if (this.initKanbanBoardId > 0) {
					this.fetchKanbanProperties();
				}
            }).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Fetching Kanban List",
					message: `Sorry, could not fetch the list of kanban board. ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});
            })
        },
        fetchKanbanProperties() {
			this.axios.get(
				`${this.rootUrl}api/v0/kanban_board/${this.kanbanBoardModel}/`
			).then(response => {
				this.kanbanColumnOptions = response.data.kanban_column;
				this.kanbanLevelOptions = response.data.kanban_level;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Fetching Kanban Properties",
					message: `Sorry, could not fetch the kanban properties. ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
				})
            });
        },
        updateDetails() {
			this.$emit("update_kanban_settings", {
				"kanbanBoardModel": parseInt(this.kanbanBoardModel),
				"kanbanColumnModel": parseInt(this.kanbanColumnModel),
				"kanbanLevelModel": parseInt(this.kanbanLevelModel),
			});
        },
    },
    mounted() {
        this.fetchKanbanBoardOptions();
    }
}
</script>
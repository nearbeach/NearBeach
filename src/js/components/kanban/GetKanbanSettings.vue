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
<!--                    <validation-rendering-->
<!--                        v-bind:error-list="v$.kanbanBoardModel.$errors"-->
<!--                    ></validation-rendering>-->
                </label>
                <n-select
					:options="kanbanBoardOptions"
					filterable
					placeholder="Search Stakeholders"
					@search="fetchKanbanBoardOptions"
					v-model:value="kanbanBoardModel"
					label-field="kanban_board_name"
                    value-field="kanban_board_id"
					class="get-stakeholders"
				/>
            </div>
        </div>
    </div>
</template>

<script>
import ValidationRendering from "../validation/ValidationRendering.vue";
import {NSelect} from "naive-ui";

export default {
    name: "GetKanbanSettings",
    components: {
        NSelect,
        ValidationRendering
    },
    data() {
        return {
            kanbanBoardModel: "",
            kanbanBoardOptions: [],
            kanbanLevelModel: "",
            kanbanLevelOptions: [],
            kanbanColumnModel: "",
            kanbanColumnOptions: [],
        };
    },
    watch: {
        kanbanBoardModel() {
            this.fetchKanbanProperties();
        },
    },
    methods: {
        fetchKanbanBoardOptions() {
            this.axios.get(
                `/api/v0/kanban_board/`
            ).then((response) => {
                this.kanbanBoardOptions = response.data.results;
                // ADD CODE
            }).catch((error) => {
                // ADD CODE
            })
        },
        fetchKanbanProperties() {
            //ADD CODE
        },
        updateDetails() {
            // ALL DATA UPSTREAM
        }
    },
    mounted() {
        this.fetchKanbanBoardOptions();
    }
}
</script>
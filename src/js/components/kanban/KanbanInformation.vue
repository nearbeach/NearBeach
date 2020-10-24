<template>
    <div>
        <div class="container">
            <div class="card">
                <div class="card-body">
                    <h1>Kanban Information</h1>
                    <hr>
                    <div class="row">
                        <!-- Instructions -->
                        <div class="col-md-4">
                            <strong>Instructions</strong>
                            <p class="text-instructions">
                                To add a new card to the board - please click on "New Card". You can link a card to an
                                existing object like a project or task by clicking on "Link Existing Object".
                            </p>
                            <p class="text-instructions">
                                You can drag and drop cards.
                            </p>
                        </div>

                        <!-- Add cards -->
                        <div class="col-md-8">
                            <h2 v-html="kanbanBoardResults[0]['fields']['kanban_board_name']"></h2><br/>
                            <div class="kanban-link">New Card</div>
                            <div class="kanban-link">Link Existing Object</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <hr>

        <!-- Rendering the Kanban Container -->
        <kanban-board v-bind:column-results="columnResults"
                      v-bind:kanban-board-results="kanbanBoardResults"
                      v-bind:kanban-card-results="kanbanCardResults"
                      v-bind:level-results="levelResults"
        ></kanban-board>
    </div>
</template>

<script>
    export default {
        name: "KanbanInformation",
        props: {
            columnResults: Array,
            kanbanBoardResults: Array,
            kanbanCardResults: Array,
            levelResults: Array,
        },
        data() {
            return {}
        },
    }
</script>

<style scoped>

</style>
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
                            <a class="kanban-link"
                               href="javascript:void(0)"
                               v-on:click="addNewKanbanCard"
                            >
                                New Card
                            </a>
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
                      v-bind:new-card-info="newCardInfo"
        ></kanban-board>

        <!-- MODALS -->
        <new-kanban-card v-bind:kanban-card-results="kanbanCardResults"
                         v-bind:column-results="columnResults"
                         v-bind:level-results="levelResults"
                         v-bind:kanban-board-results="kanbanBoardResults"
                         v-on:new_card="newCard($event)"
        ></new-kanban-card>
    </div>
</template>

<script>
    import { Modal } from "bootstrap";

    export default {
        name: "KanbanInformation",
        props: {
            columnResults: Array,
            kanbanBoardResults: Array,
            kanbanCardResults: Array,
            levelResults: Array,
        },
        data() {
            return {
                newCardInfo: [],
            }
        },
        methods: {
            addNewKanbanCard: function() {
                var addKanbanCardModal = new Modal(document.getElementById('addKanbanCardModal'));
                    addKanbanCardModal.show();
            },
            newCard: function(data) {
                this.newCardInfo = data;
            },
        }
    }
</script>

<style scoped>

</style>
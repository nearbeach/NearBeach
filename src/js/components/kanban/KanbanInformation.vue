<template>
    <div>
        <h1 class="kanban-header">{{kanbanBoardResults[0]['fields']['kanban_board_name']}}</h1>

        <!-- Rendering the Kanban Container -->
        <kanban-board v-bind:column-results="columnResults"
                      v-bind:kanban-board-results="kanbanBoardResults"
                      v-bind:kanban-card-results="localKanbanCardResults"
                      v-bind:level-results="levelResults"
                      v-bind:new-card-info="newCardInfo"
                      v-on:double_clicked_card="doubleClickedCard($event)"
        ></kanban-board>

        <!-- MODALS -->
        <new-kanban-card v-bind:kanban-card-results="kanbanCardResults"
                         v-bind:column-results="columnResults"
                         v-bind:level-results="levelResults"
                         v-bind:kanban-board-results="kanbanBoardResults"
                         v-on:new_card="newCard($event)"
        ></new-kanban-card>

        <card-information v-bind:card-information="cardInformation"
                          v-on:update_card="updateCard($event)"
        ></card-information>

        <new-kanban-link-wizard v-bind:location-id="locationId"
                                v-bind:column-results="columnResults"
                                v-bind:level-results="levelResults"
                                v-on:new_card="newCard($event)"
        ></new-kanban-link-wizard>
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
            locationId: Number,
        },
        data() {
            return {
                cardInformation: {},
                localKanbanCardResults: this.kanbanCardResults,
                newCardInfo: [],
            }
        },
        methods: {
            doubleClickedCard: function(data) {
                //Update the cardInformationId with the card id
                this.cardInformation = data;
            },
            newCard: function(data) {
                this.newCardInfo = data;
            },
            updateCard: function(data) {
                console.log("GOT HERE!");
                //Loop through the results - when the id's match. Update the data.
                this.localKanbanCardResults.forEach(row => {
                    //Check to see if the primary keys match - if they do update the data
                    if (row['pk'] == data['kanban_card_id']) {
                        row['fields']['kanban_card_text'] = data['kanban_card_text'];
                    }
                }) 
            },
        }
    }
</script>

<style scoped>

</style>

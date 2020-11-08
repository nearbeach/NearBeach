<template>
    <draggable class="list-group kanban-cell"
               group="tasks"
               :list="masterList"
               @end="onEnd($event)"
               v-bind:id="`kanban_cell_${levelId}_${columnId}`"
               v-bind:data-level="levelId"
               v-bind:data-column="columnId"
    >
        <!-- SINGLE CARDS -->
        <div class="list-group-item"
             v-for="card in masterList"
             :key="card['pk']"
             :id="card['pk']"
             v-bind:data-sort-number="card['fields']['kanban_card_sort_number']"
             v-bind:data-card-id="card['pk']"
             v-on:dblclick="doubleClickCard($event)"
        >
            {{card['fields']['kanban_card_text']}}
        </div>
    </draggable>
</template>

<script>
    const axios = require('axios');

    import { Modal } from "bootstrap";

    export default {
        name: "KanbanCard",
        props: {
            columnId: Number,
            levelId: Number,
            masterList: Array,
            newCardInfo: Array,
        },
        methods: {
            doubleClickCard: function(data) {
                //Emit the current card information
                this.$emit('double_clicked_card',data['target']['dataset']['cardId']);

                //Show the modal
                const cardInformationModal = new Modal(document.getElementById("cardInformationModal"));
                cardInformationModal.show();
            },
            onEnd: function(event) {
                console.log("Event: ",event);
                //Get the data
                var new_elem = event['to'],
                    old_elem = event['from'],
                    card_id = event['item']['dataset']['cardId'];

                //Create data_to_send
                const data_to_send = new FormData();
                data_to_send.set('new_card_column',new_elem['dataset']['column']);
                data_to_send.set('new_card_level',new_elem['dataset']['level']);
                data_to_send.set('new_card_sort_number',event['newIndex']);
                data_to_send.set('old_card_column',old_elem['dataset']['column']);
                data_to_send.set('old_card_level',old_elem['dataset']['level']);
                data_to_send.set('old_card_sort_number',event['oldIndex']);

                //Use axios to send the data to the database
                axios.post(
                    `/kanban_information/${card_id}/move_card/`,
                    data_to_send,
                ).then(response => {
                    console.log("Response: ",response);
                }).catch(error => {
                    console.log("Error: ",error);
                })
            },
        },
        watch: {
            newCardInfo: function() {
                //Only add the card if the column and the level match
                if (
                    (this.columnId == this.newCardInfo[0]['fields']['kanban_column']) &&
                    (this.levelId == this.newCardInfo[0]['fields']['kanban_level'])
                ) {
                    //The new card is for this level and column. Add it to the masterList
                    this.masterList.push(this.newCardInfo[0]);
                }
            }
        }
    }
</script>

<style scoped>

</style>
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
            <b>#{{card['pk']}}</b><br/>
            {{card['fields']['kanban_card_text']}}
            <IconifyIcon class="kanban-card-info-icon"
                         v-bind:icon="icons.infoCircle"
                         v-on:click="singleClickCard(card['pk'])"
                         v-on:dblclick="singleClickCard(card['pk'])"
            ></IconifyIcon>
        </div>

        <!-- ADD NEW CARDS + LINK OBJECTS -->
        <div class="kanban-add-new-cards">
            <a class="kanban-link btn btn-primary"
               href="javascript:void(0)"
               v-on:click="addNewKanbanCard"
            >
                New Card
            </a>
            <a class="kanban-link btn btn-warning"
               href="javascript:void(0)"
               v-on:click="addNewLink"
            >
                Link Object
            </a>
            <a class="kanban-link btn btn-danger"
               href="javascript:void(0)"
               v-on:click="archiveCards"
            >
                Archive Cards
            </a>
        </div>
    </draggable>
</template>

<script>
    const axios = require('axios');

    import { Modal } from "bootstrap";

    //Mixins
    import iconMixin from "../../mixins/iconMixin";

    export default {
        name: "KanbanCard",
        props: {
            columnId: Number,
            levelId: Number,
            masterList: Array,
            newCardInfo: Array,
        },
        mixins: [
            iconMixin,
        ],
        methods: {
            addNewKanbanCard: function() {
                //Update the modal's data-attributes to reflect the column ID and Level ID
                var addKanbanCardModal = document.getElementById('addKanbanCardModal');
                addKanbanCardModal['dataset']['kanbanLevel'] = this.levelId;
                addKanbanCardModal['dataset']['kanbanColumn'] = this.columnId;

                //Get the Modal from the above modal
                var addKanbanCardModal = new Modal(addKanbanCardModal);
                addKanbanCardModal.show();
            },
            addNewLink: function() {
                //Update the modal's data-attributes to reflect the column ID and Level ID
                var newLinkModal = document.getElementById('newLinkModal');
                newLinkModal['dataset']['kanbanLevel'] = this.levelId;
                newLinkModal['dataset']['kanbanColumn'] = this.columnId;

                //Get the Modal from the above modal
                var newLinkModal = new Modal(newLinkModal);
                newLinkModal.show();
            },
            archiveCards: function() {
                // Create data_to_send
                const data_to_send = new FormData();

                // Loop through the master list and get all card ids
                this.masterList.forEach(row => {
                    data_to_send.append('kanban_card_id', row['pk']);
                });

                // Use axios to contact backend
                axios.post(
                    `/kanban_information/archive_kanban_cards/`,
                    data_to_send,
                ).then(response => {
                    document.location.reload(true)
                }).catch(error => {
                    console.log("ERROR: ",error); 
                })
            },
            doubleClickCard: function(data) {
                //Filter out the data we want to send up stream
                const filtered_data = this.masterList.filter(row => {
                    return row['pk'] == data['target']['dataset']['cardId'];
                })[0];

                //Setup data to send upstream
                this.sendDataUpstream(filtered_data);
            },
            onEnd: function(event) {
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
            sendDataUpstream: function(filtered_data) {
                // Update VueX
                this.$store.commit({
                    type: 'updateCard',
                    'cardId': filtered_data['pk'],
                    'cardTitle': filtered_data['fields']['kanban_card_text'],
                    'cardDescription': filtered_data['fields']['kanban_card_description'],
                    'cardColumn': filtered_data['fields']['kanban_column'],
                    'cardLevel': filtered_data['fields']['kanban_level'],
                })

                //Emit the current card information
                //this.$emit('double_clicked_card',data_to_send);
                
                //Show the modal
                const cardInformationModal = new Modal(document.getElementById("cardInformationModal"));
                cardInformationModal.show();
            },
            singleClickCard: function(data) {
                //Filter out the data we want to send up stream
                const filtered_data = this.masterList.filter(row => {
                    return row['pk'] == data;
                })[0];

                //Setup data to send upstream
                this.sendDataUpstream(filtered_data);
            }
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

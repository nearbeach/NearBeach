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
    
    //VUEX MAP GETTERS
    import { mapGetters } from 'vuex';

    export default {
        name: "KanbanCard",
        props: {
            columnId: Number,
            levelId: Number,
            //masterList: Array,
            newCardInfo: Array,
        },
        data() {
            return {
                //masterList: [],
            }
        },
        computed: {
            ...mapGetters({
                allCards: 'getCards',
            }),
            masterList: function() {
                //Filter the data
                let return_array = this.allCards.filter(card => {
                    return card['fields']['kanban_column'] == this.columnId &&
                           card['fields']['kanban_level'] == this.levelId;
                })

                //Make sure it is sorted
                return_array = return_array.sort((a,b) => {
                    return a['fields']['kanban_card_sort_number'] - b['fields']['kanban_card_sort_number'];
                })

                return return_array;
            },
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
            dragDifferentColumn(data) {
                //Short hand - making it easy to read code later
                let new_card_column = data.get('new_card_column'),
                    new_card_level = data.get('new_card_level'),
                    new_card_sort_number = parseInt(data.get('new_card_sort_number')),
                    old_card_column = data.get('old_card_column'),
                    old_card_level = data.get('old_card_level'),
                    old_card_sort_number = parseInt(data.get('old_card_sort_number')),
                    card_id = data.get('card_id');

                //Create return array
                let return_array = [];

                //Move new column first
                //Filter for all data effected in the new column
                let filter_new_column = this.allCards.filter(row => {
                    //return where column = new_card_column, and sort level >= new sort level
                    return row['fields']['kanban_column'] == new_card_column &&
                           row['fields']['kanban_level'] == new_card_level &&
                           row['fields']['kanban_card_sort_number'] >= new_card_sort_number;
                });

                //Loop through the filtered new columns and add the required data to the return array
                filter_new_column.forEach(row => {
                    //Move the cards up by one
                    return_array.push({
                        card_id: row['pk'],
                        kanban_column: new_card_column,
                        kanban_level: new_card_level,
                        kanban_card_sort_number: row['fields']['kanban_card_sort_number'] + 1, 
                    });
                })

                //Filter for all data effected in old column
                let filter_old_column = this.allCards.filter(row => {
                    //Return where column = old_card_column, and the sort level >= old sort level
                    return row['fields']['kanban_column'] == old_card_column &&
                           row['fields']['kanban_level'] == old_card_level &&
                           row['fields']['kanban_card_sort_number'] >= old_card_sort_number;
                })

                //Loop through the filter old columns and add the required data to return array
                filter_old_column.forEach(row => {
                    if (row['pk'] == card_id) {
                        //Move this to the new column
                        return_array.push({
                            card_id: row['pk'],
                            kanban_column: new_card_column,
                            kanban_level: new_card_level,
                            kanban_card_sort_number: new_card_sort_number, 
                        });

                    } else {
                        //Move the cards down by 1
                        return_array.push({
                            card_id: row['pk'],
                            kanban_column: old_card_column,
                            kanban_level: old_card_level,
                            kanban_card_sort_number: row['fields']['kanban_card_sort_number'] - 1, 
                        });
                    }
                })


                return return_array;
            },
            dragSameColumn(data) {
                //Short hand - making it easy to read code later
                let new_sort = parseInt(data.get('new_card_sort_number')),
                    old_sort = parseInt(data.get('old_card_sort_number')),
                    column = parseInt(data.get('new_card_column')),
                    level = parseInt(data.get('new_card_level')),
                    card_id = parseInt(data.get('card_id'));

                //Determine the delta - -1 or 1.
                //Negative number if old_sort is less than new sort, i.e. move
                //everything back one
                let delta = 1 - 2*(old_sort < new_sort);

                //Get the largest and smallest values
                let largest = (new_sort >= old_sort)*new_sort + (new_sort < old_sort)*old_sort,
                    smallest = (new_sort >= old_sort)*old_sort + (new_sort < old_sort)*new_sort;

                //If they are the same (i.e. drag and dropped in same place) - return
                if (largest == smallest) {
                    return [];
                }

                //Filter for the data we need
                let filtered_data = this.allCards.filter(row => {
                    //Return when same column and level, whilst also in range of smallest and largest
                    return row['fields']['kanban_column'] === column &&
                           row['fields']['kanban_level'] === level &&
                           row['fields']['kanban_card_sort_number'] >= smallest &&
                           row['fields']['kanban_card_sort_number'] <= largest;
                })

                //Create the return array
                let return_array = [];

                //Loop through the filtered data, and apply the changes required
                filtered_data.forEach(row => {
                    console.log("Row: ",row['pk']);
                    if (row['pk'] == card_id) {
                        //Make sure this card has the new sort number
                        return_array.push({
                            card_id: row['pk'],
                            kanban_column: column,
                            kanban_level: level,
                            kanban_card_sort_number: new_sort, 
                        });
                    } else {
                        //Not the card we moved, apply the delta to move the sort order
                        return_array.push({
                            card_id: row['pk'],
                            kanban_column: column,
                            kanban_level: level,
                            kanban_card_sort_number: row['fields']['kanban_card_sort_number'] + delta, 
                        });
                    }
                })

                return return_array;
            },
            onEnd: function(event) {
                /* Update the sort order
                If both the old and new level/column destinations are the same,
                we take the difference between the two values. Otherwise we apply
                two sort orders to both the old and the new*/
                
                //Get the y=data
                var new_elem = event['to'],
                    old_elem = event['from'],
                    card_id = event['item']['dataset']['cardId'];

                //Setup variables (for shorthand)
                let new_card_column = new_elem['dataset']['column'],
                    new_card_level = new_elem['dataset']['level'],
                    new_card_sort_number = event['newIndex'],
                    old_card_column = old_elem['dataset']['column'],
                    old_card_level = old_elem['dataset']['level'],
                    old_card_sort_number = event['oldIndex'];


                //Create data_to_send
                const data_to_send = new FormData();
                data_to_send.set('new_card_column', new_card_column);
                data_to_send.set('new_card_level', new_card_level);
                data_to_send.set('new_card_sort_number', new_card_sort_number);
                data_to_send.set('old_card_column', old_card_column);
                data_to_send.set('old_card_level', old_card_level);
                data_to_send.set('old_card_sort_number', old_card_sort_number);
                data_to_send.set('card_id', card_id);

                //Use axios to send the data to the database
                axios.post(
                    `/kanban_information/${card_id}/move_card/`,
                    data_to_send,
                ).then(response => {
                    //Define cards_to_change
                    let cards_to_change = [];

                    //Depending if the card moves columns depends what we do
                    if ((new_card_column == old_card_column) && 
                        (new_card_level == old_card_level)) {
                        //The card stayed in the same place.
                        console.log("Drag Same Column");
                        cards_to_change = this.dragSameColumn(data_to_send);
                    } else {
                        //The card move to a different place
                        console.log("Drag Different Column");
                        cards_to_change = this.dragDifferentColumn(data_to_send);
                    }

                    console.log("Cards to Change: ",cards_to_change);

                    //ADD CODE - loop through the cards to change
                    cards_to_change.forEach(row => {
                        this.$store.commit({
                            type: 'updateKanbanCard',
                            card_id: row['card_id'],
                            kanban_column: row['kanban_column'], 
                            kanban_level: row['kanban_level'],
                            kanban_card_sort_number: row['kanban_card_sort_number'],
                        })
                    })
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
            },
        },
    }
</script>

<style scoped>

</style>

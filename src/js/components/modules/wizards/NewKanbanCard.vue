<template>
    <div class="modal fade" id="addKanbanCardModal" tabindex="-1" aria-labelledby="addKanbanCardModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="users"></i> Add Kanban Card Wizard</h2>
                    <button type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            id="addKanbanCardCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Please note</strong>
                            <p class="text-instructions">
                                The card names can not be the same as something that already exists on the board.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <label>Kanban Card Text</label>
                            <input v-model="kanbanCardTextModel"
                                   class="form-control"
                            >
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-on:click="addKanbanCard"
                            v-bind:disabled="disableAddButton"
                    >
                        Add Link
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    export default {
        name: "NewKanbanCard",
        props: {
            columnResults: Array,
            kanbanCardResults: Array,
            levelResults: Array,
            kanbanBoardResults: Array,
        },
        data() {
            return {
                disableAddButton: true,
                kanbanCardTextModel: '',
            }
        },
        methods: {
            addKanbanCard: function() {
                //Create the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('kanban_card_text',this.kanbanCardTextModel);
                data_to_send.set('kanban_level',this.levelResults[0]['pk']);
                data_to_send.set('kanban_column',this.columnResults[0]['pk']);

                //Send the data
                axios.post(
                    `/kanban_information/${this.kanbanBoardResults[0]['pk']}/new_card/`,
                    data_to_send,
                ).then(response => {
                    //Find the first card section and place the new card at the end
                    var card_elem = document.getElementById(
                        `kanban_cell_${this.levelResults[0]['pk']}_${this.columnResults[0]['pk']}`
                    );

                    //Add the element
                    var card_id = response['data'][0]['pk'],
                        card_text = response['data'][0]['fields']['kanban_card_text'];

                    card_elem.innerHTML = `${card_elem.innerHTML}<div id="${card_id}" class="list-group-item">${card_text}</div>`

                    //Blank the model
                    this.kanbanCardTextModel = '';

                    //Close the modal
                    document.getElementById('addKanbanCardCloseButton').click();
                }).catch(error => {
                    console.log("ERROR: ",error);
                });
            },
        },
        watch: {
            kanbanCardTextModel: function() {
                // If the model is blank OR the text already exists - turn disableAddButton to true
                this.disableAddButton = false; //People can click the "Add" button

                if (this.kanbanCardTextModel.length == 0) {
                    this.disableAddButton = true;
                }

                //Check to make sure it does not exist
                var filtered_results = this.kanbanCardResults.filter(row => {
                    return row['fields']['kanban_card_text'] == this.kanbanCardTextModel;
                });

                if (filtered_results.length > 0) {
                    this.disableAddButton = true;
                }

                //If there are no rows or levels - we don't want the user to submit a card
                if (this.columnResults.length == 0 || this.levelResults.length == 0) {
                    this.disableAddButton = true;
                }
            },
        }
    }
</script>

<style scoped>

</style>
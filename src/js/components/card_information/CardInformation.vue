<template>
   <div class="modal fade" id="cardInformationModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><IconifyIcon v-bind:icon="icons.usersIcon"></IconifyIcon> Card Information</h2>
                    <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            id="cardInformationModalCloseButton"
                    >
                        <span aria-hidden="true"></span>
                    </button>
                </div>
                <div class="modal-body">
                    <!-- TAB MENU -->
                    <ul id="card_information_tabs" 
                        class="nav nav-tabs" 
                        role="tablist"
                    >
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" 
                                    id="details-tab" 
                                    data-bs-toggle="tab" 
                                    data-bs-target="#card_details" 
                                    type="button" 
                                    role="tab" 
                                    aria-controls="home" 
                                    aria-selected="true"
                            >Details</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" 
                                    id="description-tab" 
                                    data-bs-toggle="tab" 
                                    data-bs-target="#card_description" 
                                    type="button" 
                                    role="tab" 
                                    aria-controls="profile" 
                                    aria-selected="false"
                            >Description</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" 
                                    id="notes-tab" 
                                    data-bs-toggle="tab" 
                                    data-bs-target="#card_notes" 
                                    type="button" 
                                    role="tab" 
                                    aria-controls="contact" 
                                    aria-selected="false"
                            >Notes</button>
                        </li>
                    </ul>
                    <hr>

                    <!-- CONTENT OF TABS -->
                    <div class="tab-content" id="myTabContent">
                        <div class="tab-pane fade show active" 
                            id="card_details" 
                            role="tabpanel" 
                            aria-labelledby="details-tab"
                        >
                            <card-details></card-details>
                        </div>

                        <div class="tab-pane fade" 
                             id="card_description" 
                             role="tabpanel" 
                             aria-labelledby="description-tab"
                        >
                            <card-description></card-description>
                        </div>

                        <div class="tab-pane fade" 
                             id="card_notes" 
                             role="tabpanel" 
                             aria-labelledby="notes-tab"
                        >
                            <card-notes></card-notes>
                        </div>
                    </div>
                </div>
           </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    //Mixins
    import iconMixin from "../../mixins/iconMixin";

    export default {
        name: 'CardInformation',
        mixins: [
            iconMixin,
        ],
        data() {
            return {
                cardId: '',
                cardDescriptionModel: '',
                cardNoteModel: '',
                cardTitleModel: '',
                noteHistoryResults: [],
            }
        },
        watch: {
            cardInformation: function() {
                console.log("Card Information Changed");
                //Update the local information
                this.cardId = this.cardInformation['cardId'];
                this.cardTitleModel = this.cardInformation['cardTitle'];

                //Bug fix - needs to blank it out or the value does nto blank out correctly
                if (this.cardInformation['cardDescription'] === null) {
                    //Can not seem to blank out the model correctly?
                    this.cardDescriptionModel = "No Description";
                } else {
                    this.cardDescriptionModel = `${this.cardInformation['cardDescription']}`;
                }


                //Now update the card notes
                this.getCardNotes();
            },
        },
        methods: {
            addNote: function() {
                //Setup data to send
                const data_to_send = new FormData();
                data_to_send.set('note',this.cardNoteModel);

                //Use axios to send the data
                axios.post(
                    `/object_data/kanban_card/${this.cardId}/add_notes/`,
                    data_to_send,
                ).then(response => {
                    //Add the response to the end of the noteHistoryResults
                    this.noteHistoryResults.push(response['data'][0]);

                    //Clear the card note model
                    this.cardNoteModel = '';
                }).catch(error => {
                    console.log("Error: ",error);
                })
            },
            getCardNotes: function() {
                //Clear the current list of notes
                this.noteHistoryResults = [];

                //Use axios to get the card list
                axios.post(
                    `/object_data/kanban_card/${this.cardId}/note_list/`
                ).then(response => {
                    //Save the data into noteHistoryResults
                    this.noteHistoryResults = response['data'];
                }).catch(error => {
                    console.log("Error: ",error);
                })
            },
            updateCard: function() {
                //Create the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('kanban_card_text',this.cardTitleModel);
                data_to_send.set('kanban_card_description', this.cardDescriptionModel);
                data_to_send.set('kanban_card_id',this.cardId);

                //Use Axios to send data
                axios.post(
                    `/kanban_information/update_card/`,
                    data_to_send,
                ).then(response => {
                    //Send the new data upstream
                    this.$emit('update_card',{
                        'kanban_card_id': this.cardId,
                        'kanban_card_text': this.cardTitleModel,
                    });

                    //Close the modal
                    document.getElementById("cardInformationModal").click();
                }).catch(error => {
                    console.log("Error: ",error);
                })
            },
        }
    }
</script>

<style scoped>

</style>

<template>
   <div class="modal fade" id="cardInformationModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><Icon v-bind:icon="icons.usersIcon"></Icon> Card Information</h2>
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
                            <card-details v-on:update_card="updateCard"
                            ></card-details>
                        </div>

                        <div class="tab-pane fade" 
                             id="card_description" 
                             role="tabpanel" 
                             aria-labelledby="description-tab"
                        >
                            <card-description v-on:update_card="updateCard"
                            ></card-description>
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
    import axios from 'axios';
    import { Icon } from '@iconify/vue';

    //VueX
    import { mapGetters } from 'vuex';

    //Mixins
    import iconMixin from "../../mixins/iconMixin";

    export default {
        name: 'CardInformation',
        components: {
            Icon,
        },
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
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
            })
        },
        methods: {
            updateCard: function() {
                //Get all data from VueX
                const all_data = this.$store.getters.getAllCardData;

                //Setup data_to_send
                const data_to_send = new FormData()
                data_to_send.set('kanban_card_text', all_data.cardTitle);
                data_to_send.set('kanban_card_description', all_data.cardDescription);
                data_to_send.set('kanban_level', all_data.cardLevel.value);
                data_to_send.set('kanban_column', all_data.cardColumn.value);
                data_to_send.set('kanban_card_id', all_data.cardId);

                //Use Axios to send data to backend
                axios.post(
                    `${this.rootUrl}kanban_information/update_card/`,
                    data_to_send,
                ).then(response => {
                    //Send the new data upstream
                    this.$emit('update_card',{
                        'kanban_card_id': all_data.cardId,
                        'kanban_card_text': all_data.cardTitle,
                        'kanban_column': all_data.cardColumn,
                        'kanban_level': all_data.cardLevel,
                    });

                    document.getElementById("cardInformationModalCloseButton").click();
                }).catch(error => {
                    
                })
            }
        }
    }
</script>

<style scoped>

</style>

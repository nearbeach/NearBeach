<template>
    <div>
        <h2><i data-feather="git-branch"></i> Note History</h2>
        <p class="text-instructions">
            The following are saved notes against this {{destination}}. Add notes by clicking on the button below.
        </p>

        <list-notes v-bind:note-history-results="noteHistoryResults"
                    v-bind:destination="destination"
        ></list-notes>

        <!-- ADD NOTE HISTORY -->
        <!-- TO DO - limit it to certain users -->
        <hr>
        <div class="row submit-row">
            <div class="col-md-12">
                <a href="javascript:void(0)"
                   class="btn btn-primary save-changes"
                   v-on:click="createNewNote"
                >Add Note to {{destination}}</a>
            </div>
        </div>

        <!-- Modals for Notes section -->
        <new-history-note-wizard v-bind:location-id="locationId"
                                 v-bind:destination="destination"
                                 v-on:update_note_history_results="updateNoteHistoryResults($event)"
        ></new-history-note-wizard>
    </div>
</template>

<script>
    // JavaScript Libraries
    import {Modal} from "bootstrap";
    import errorModalMixin from "../../../mixins/errorModalMixin";
    const axios = require('axios');

    export default {
        name: "MiscModule",
        components: {},
        props: [
            'destination',
            'locationId',
        ],
        mixins: [
            errorModalMixin,
        ],
        data() {
            return {
                noteHistoryResults: [],
            };
        },
        methods: {
            createNewNote: function() {
                var newNoteModal = new Modal(document.getElementById('newNoteModal'));
                    newNoteModal.show();
            },
            getNoteHistoryResults: function() {
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/note_list/`,
                ).then(response => {
                    this.noteHistoryResults = response['data'];
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })
            },
            updateNoteHistoryResults: function(data) {
                //Add the extra data
                this.noteHistoryResults.push(data[0]);
            }
        },
        mounted() {
            this.getNoteHistoryResults();
        }

    }
</script>

<style scoped>

</style>

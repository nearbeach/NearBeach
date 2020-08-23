<template>
    <div>
        <h2><i data-feather="git-branch"></i> Note History</h2>
        <p class="text-instructions">
            The following are saved notes against this {{destination}}. Add notes by clicking on the button below.
        </p>

        <!-- NOTE HISTORY -->
        <div v-if="noteHistoryResults.length == 0"
             class="module-spacer"
        >
            <div class="alert alert-dark">
                Sorry - but there are no notes for this {{destination}}.
            </div>
        </div>
        <div v-else>
            ADD IN CODE
        </div>

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
        ></new-history-note-wizard>
    </div>
</template>

<script>
    // JavaScript Libraries
    import {Modal} from "bootstrap";

    export default {
        name: "MiscModule",
        components: {},
        props: [
            'destination',
            'locationId',
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
            updateNoteHistoryResults: function() {

            }
        }

    }
</script>

<style scoped>

</style>
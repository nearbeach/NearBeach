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
        <!-- NEW HISTORY NOTE -->
        <div class="modal fade"
             id="newNoteModal"
             tabindex="-1"
             role="dialog"
             aria-labelledby="exampleModalLabel"
             aria-hidden="true"
        >
            <div class="modal-dialog modal-lg"
                 role="document"
            >
                <div class="modal-content">
                    <div class="modal-header">
                        <h2><i data-feather="git-branch"></i> New Note</h2>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p class="text-instructions">
                            Use the text editor to type out your note. Click on the submit button to submit the note.
                        </p>
                        <editor
                           :init="{
                             height: 300,
                             menubar: false,
                             toolbar: 'undo redo | ' +
                              'bold italic backcolor | alignleft aligncenter ' +
                              'alignright alignjustify | bullist numlist outdent indent | ',
                           }"
                           v-model="newNoteModel"
                        />
                    </div>
                    <div class="modal-footer">
                        <button type="button"
                                class="btn btn-primary"
                                v-bind:disabled="newNoteModel == ''"
                        >
                            Submit Note
                        </button>
                        <button type="button"
                                class="btn btn-secondary"
                                data-dismiss="modal"
                        >
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    // JavaScript Libraries
    const axios = require('axios');
    import {Modal} from "bootstrap";

    export default {
        name: "MiscModule",
        components: {
            axios,
        },
        props: [
            'destination',
            'location_id',
        ],
        data() {
            return {
                newNoteModel: '',
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
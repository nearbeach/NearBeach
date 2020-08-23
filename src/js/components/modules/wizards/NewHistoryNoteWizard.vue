<template>
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
</template>

<script>
    //JavaScript components
    const axios = require('axios');

    export default {
        name: "NewHistoryNoteWizard",
        props: [
            'locationId',
            'destination',
        ],
        data() {
            return {
                newNoteModel: '',
            }
        },
        methods: {
            submitNote: function() {
                //Construct the form data to send
                const data_to_send = new FormData();

                //Add the data to data_to_send
                // NEED TO CREATE A NOTES TABLE THAT CONNECTS TO ANY OBJECT!
            }
        }
    }
</script>

<style scoped>

</style>
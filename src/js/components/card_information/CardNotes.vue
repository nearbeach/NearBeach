<template>
    <div>
        <div class="row">
            <div class="col-md-4">
                <strong>Notes</strong>
                <p class="text-instructions">
                    To add a note - type your note in the Note Box and hit the "Submit Note"
                    button.
                </p>
            </div>
            <div class="col-md-8">
                <label>Note Box</label>
                <editor
                    :init="{
                        height: 250,
                        menubar: false,
                        toolbar: 'undo redo | formatselect | ' +
                        'bold italic backcolor | alignleft aligncenter ' +
                        'alignright alignjustify | bullist numlist outdent indent | ',
                    }"
                    v-bind:content_css="false"
                    v-bind:skin="false"
                    v-model="cardNoteModel"
                />
            </div>
        </div>
        <hr>
        <div class="row">
            <div class="col-md-12">
                <br/>
                <button class="btn btn-primary save-changes"
                        v-on:click="addNote"
                        v-bind:disabled="cardNoteModel===''"
                >
                    Add Note
                </button>
            </div>
        </div>
        <hr>

        <!-- NOTE HISTORY -->
        <list-notes v-bind:note-history-results="noteHistoryResults"
                    v-bind:destination="'card'"
        ></list-notes> 
    </div>
</template>

<script>
    export default {
        name: 'CardNotes',
        props: {},
        data() {
            return {
                cardNoteModel: '',
                noteHistoryResults: this.$store.state.cardNoteModel,
            }
        },
        methods: {
            addNote: function() {
                //ADD CODE
            }
        },
    }
</script>


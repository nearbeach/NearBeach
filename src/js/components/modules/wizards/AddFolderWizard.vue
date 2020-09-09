<template>
    <div class="modal fade" id="addFolderModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="users"></i> Add Folder Wizard</h2>
                    <button type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            id="addFolderCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Creating a folder</strong>
                            <p class="text-instructions">
                                Give the folder an appropriate name. When done, click on the "Save" button. It will be
                                added to the current folder.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <div class="form-group">
                                <label for="folder">Folder Name</label>
                                <input type="text"
                                       v-model="folderModel"
                                       class="form-control"
                                       id="folder"
                                >
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-bind:disabled="folderModel==''"
                            v-on:click="addFolder"
                    >
                        Add Folder
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    export default {

        name: "AddFolderWizard",
        props: [
            'currentFolder',
            'destination',
            'locationId',
        ],
        data() {
            return {
                folderModel: '',
            };
        },
        methods: {
            addFolder: function() {
                //ADD CODE
            }
        }
    }
</script>

<style scoped>

</style>
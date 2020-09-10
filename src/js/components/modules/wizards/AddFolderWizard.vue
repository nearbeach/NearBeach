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
                                <label for="folder_description">Folder Name</label>
                                <input type="text"
                                       v-model="folderDescriptionModel"
                                       class="form-control"
                                       id="folder_description"
                                       maxlength="50"
                                >
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-bind:disabled="folderDescriptionModel==''"
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
                folderDescriptionModel: '',
            };
        },
        methods: {
            addFolder: function() {
                //Construct the data to send
                const data_to_send = new FormData();
                data_to_send.set('folder_description',this.folderDescriptionModel);

                if (this.currentFolder != null && this.currentFolder != '') {
                    data_to_send.set('parent_folder',this.currentFolder);
                }

                //Send the data in POST
                axios.post(
                    `/documentation/${this.destination}/${this.locationId}/add_folder/`,
                    data_to_send,
                ).then(response => {
                    //Send the data up stream to get appended
                    this.$emit('update_folder_list',response['data']);

                    //Clear the model
                    this.folderDescriptionModel = '';

                    //Close the modal
                    document.getElementById('addFolderCloseButton').click();
                }).catch(error => {
                    console.log("Error: ",error);
                })
            }
        }
    }
</script>

<style scoped>

</style>
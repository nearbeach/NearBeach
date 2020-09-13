<template>
    <div class="modal fade" id="uploadDocumentModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="users"></i> Upload Document Wizard</h2>
                    <button type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            id="uploadDocumentCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Uploading File</strong>
                            <p class="text-instructions">
                                You will be able to upload a file against this {{destination}}. It will appear in the
                                current folder.
                            </p>
                            <p v-if="documentModel.length == 0">
                                1. Please click on "Upload File" button to upload a file
                            </p>
                            <p v-else>
                                2. Please modify the document descript to be more human readable. Or click the "Reset"
                                button to remove the uploaded file.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <div class="form-file"
                                 v-if="documentModel.length ==0"
                            >
                                <input type="file"
                                       class="form-file-input"
                                       id="document"
                                       v-on:change="handleFileUploads($event.target.files)"
                                >
                                <label class="form-file-label"
                                       for="document"
                                >
                                    <span class="form-file-text">Choose file...</span>
                                    <span class="form-file-button">Browse</span>
                                </label>
                            </div>
                            <div class="form-group"
                                 v-else
                             >
                                <!-- DOCUMENT DESCRIPTION -->
                                <div class="form-group">
                                    <label for="documentDescription">Document Description</label>
                                    <input id="documentDescription"
                                           v-model="documentDescriptionModel"
                                           type="text"
                                           class="form-control"
                                    >
                                </div>

                                <!-- RESET FORM BUTTON -->
                                <br/>
                                <div class="form-row">
                                    <button v-on:click="resetForm"
                                            class="btn btn-warning"
                                    >
                                        Reset Form
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-bind:disabled="disableUploadButton"
                            v-on:click="uploadFile"
                    >
                        Upload File
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    export default {
        name: "UploadDocumentWizard",
        props: [
            'currentFolder',
            'destination',
            'excludeDocuments',
            'locationId',
        ],
        data() {
            return {
                disableUploadButton: true,
                documentModel: [],
                documentDescriptionModel: '',
            };
        },
        methods: {
            handleFileUploads: function(fileList) {
                //Update the document modal
                this.documentModel = fileList[0];

                //Extract the file name and place into the document description for the user
                this.documentDescriptionModel = fileList[0]['name'];
            },
            resetForm: function() {
                //Blank out all the models
                this.documentModel = '';
                this.documentDescriptionModel = '';
            },
            uploadFile: function() {
                //Create the data to send
                const data_to_send = new FormData();
                data_to_send.set('document',this.documentModel,this.documentDescriptionModel);
                data_to_send.set('document_description',this.documentDescriptionModel);

                //If there is a current/partent folder - then add it to the data to send
                if (this.currentFolder != '' && this.currentFolder != null) {
                    data_to_send.set('parent_folder',this.currentFolder);
                }

                //Use axios to send it to the backend
                axios.post(
                    `/documentation/${this.destination}/${this.locationId}/upload/`,
                    data_to_send,
                ).then(response => {
                    //Send the data upstream
                    this.$emit('update_document_list',response['data']);

                    //Close the modal
                    document.getElementById('uploadDocumentCloseButton').click();
                }).catch(error => {
                    console.log("Error: ",error);
                })
            }
        },
        updated() {
            var match = this.excludeDocuments.filter(row => {
                return row['document_key__document_description'] == this.documentDescriptionModel;
            });

            this.disableUploadButton = this.documentModel == '' || this.documentDescriptionModel.length == 0 ||
                    match.length > 0;
        }
    }
</script>

<style scoped>

</style>
<template>
    <div class="modal fade" id="addLinkModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="users"></i> Add Link Wizard</h2>
                    <button type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            id="addLinkCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Add Link</strong>
                            <p class="text-instruction">
                                Add hyperlinks to other documents and sources located in on the internet/cloud.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <div class="form-group">
                                <label for="document_url_location">Document URL</label>
                                <input id="document_url_location"
                                       v-model="documentUrlLocationModel"
                                       class="form-control"
                                >
                            </div>
                            <div class="form-group">
                                <label for="document_description">Document Description</label>
                                <input id="document_description"
                                       v-model="documentDescriptionModel"
                                       class="form-control"
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
                            v-on:click="addLink"
                    >
                        Add Link
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    export default {
        name: "AddLinkWizard",
        props: [
            'currentFolder',
            'destination',
            'excludeDocuments',
            'locationId',
        ],
        data() {
            return {
                linkModel: '',
                disableAddButton: true,
                documentDescriptionModel: '',
                documentUrlLocationModel: '',

            };
        },
        methods: {
            addLink: function() {
                const data_to_send = new FormData();
                data_to_send.set('document_description',this.documentDescriptionModel);
                data_to_send.set('document_url_location',this.documentUrlLocationModel);
                data_to_send.set('parent_folder',this.currentFolder);

                axios.post(
                    `/documentation/${this.destination}/${this.locationId}/add_link/`,
                    data_to_send,
                ).then(response => {
                    //Emit the results up stream
                    this.$emit('update_document_list',response['data']);

                    //Close the modal
                    document.getElementById("addLinkCloseButton").click();
                }).catch(error => {
                    console.log("Error: ",error);
                });
            },
        },
        updated() {
            //We need to make sure both fields are not blank & to make sure the description is not duplicated
            var match = this.excludeDocuments.filter(row => {
                return row['document_key__document_description'] == this.documentDescriptionModel;
            });

            //Determining the add button will be disabled
            // this.disableAddButton = match.length > 0 ||         //If there are any matches
            //     this.documentDescriptionModel.length > 0 ||     //If there is no description
            //     !this.validURL(this.documentUrlLocationModel);  //Validate the URL
            //WE SHOULD USE THE VALIDATION LIBRARY TO VALIDATE EVERYTHING
            this.disableAddButton = false;
        },
    }
</script>

<style scoped>

</style>
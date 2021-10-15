<template>
    <div class="modal fade" id="addLinkModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><IconifyIcon v-bind:icon="icons.userIcon"></IconifyIcon> Add Link Wizard</h2>
                    <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            id="addLinkCloseButton"
                    >
                        <span aria-hidden="true"></span>
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
                                <label for="document_url_location">
                                    Document URL
                                    <span class="error"
                                          v-if="!$v.documentUrlLocationModel.required && $v.documentUrlLocationModel.$dirty"
                                    > Please suppy a URL.</span>
                                    <span class="error"
                                          v-if="!$v.documentUrlLocationModel.url && $v.documentUrlLocationModel.$dirty"
                                    > Please suppy a proper URL.</span>

                                </label>
                                <input id="document_url_location"
                                       v-model="documentUrlLocationModel"
                                       class="form-control"
                                >
                            </div>
                            <div class="form-group">
                                <label for="document_description">
                                    Document Description
                                    <span class="error"
                                          v-if="!$v.documentDescriptionModel.required && $v.documentDescriptionModel.$dirty"
                                    > Please suppy a description of the link.</span>
                                    <span class="error"
                                          v-if="duplicateDescription"
                                    > Sorry - but this is a duplicated description.</span>

                                </label>
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
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-on:click="addLink"
                            v-bind:disabled="disableAddButton"
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

    //Mixins
    import errorModalMixin from "../../../mixins/errorModalMixin";
    import iconMixin from "../../../mixins/iconMixin";

    //Validation
    import { required, url } from 'vuelidate/lib/validators';

    export default {
        name: "AddLinkWizard",
        props: [
            'currentFolder',
            'destination',
            'excludeDocuments',
            'locationId',
        ],
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        data() {
            return {
                linkModel: '',
                disableAddButton: true,
                documentDescriptionModel: '',
                documentUrlLocationModel: '',
                duplicateDescription: false,

            };
        },
        validations: {
            documentDescriptionModel: {
                required,
            },
            documentUrlLocationModel: {
                required,
                url,
            },
        },
        methods: {
            addLink: function() {
                const data_to_send = new FormData();
                data_to_send.set('document_description',this.documentDescriptionModel);
                data_to_send.set('document_url_location',this.documentUrlLocationModel);

                //Only set the parent folder variable if there exists a variable in current folder
                if (this.currentFolder !== null && this.currentFolder != '') {
                    data_to_send.set('parent_folder',this.currentFolder);
                }

                axios.post(
                    `/documentation/${this.destination}/${this.locationId}/add_link/`,
                    data_to_send,
                ).then(response => {
                    //Emit the results up stream
                    this.$emit('update_document_list',response['data']);

                    //Clear the data
                    this.documentDescriptionModel = '';
                    this.documentUrlLocationModel = '';

                    //Close the modal
                    document.getElementById("addLinkCloseButton").click();
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                });
            },
        },
        updated() {
            //We need to make sure both fields are not blank & to make sure the description is not duplicated
            var match = this.excludeDocuments.filter(row => {
                return row['document_key__document_description'] == this.documentDescriptionModel;
            });

            //Notify the user of duplicate descriptions (if there is any)
            this.duplicateDescription = match.length > 0;

            // Check the validation
            this.$v.$touch();

            //Disable the button (if it does not meet our standards)
            this.disableAddButton = this.$v.$invalid || match.length > 0;
        },
    }
</script>

<style scoped>

</style>

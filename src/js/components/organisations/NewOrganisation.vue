<template>
    <div class="card">
        <div class="card-body">
            <!-- TITLE -->
            <h1>New Organisation</h1>
            <hr>

            <!-- FIELDS SECTION -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Description</strong>
                    <p class="text-instructions">
                        Please fill out all the required fields. Please only use a generic email for the organisation
                        email field. e.g. support@companyxyz.com
                    </p>
                </div>
                <div class="col-md-8">
                    <!-- ORGANISATION NAME -->
                    <div class="form-group">
                        <label for="id_organisation_name">
                            Organisation Name:
                            <span class="error"
                                  v-if="!$v.organisationNameModel.required && $v.organisationNameModel.$dirty"
                                > Please suppy a title.
                            </span>
                        </label>
                        <input id="id_organisation_name"
                               name="organisation_name"
                               type="text"
                               class="form-control"
                               v-model="organisationNameModel"
                        >
                    </div>
                    <br/>

                    <div class="row">
                        <!-- ORGANISATION WEBSITE -->
                        <div class="form-group col-md-6">
                            <label for="id_organisation_website">
                                Organisation Website:
                                <span class="error"
                                      v-if="!$v.organisationWebsiteModel.required && $v.organisationWebsiteModel.$dirty"
                                      > Please supply
                                </span>
                                <span class="error"
                                      v-if="!$v.organisationWebsiteModel.url && $v.organisationWebsiteModel.$dirty"
                                      > Please format at URL
                                </span>
                            </label>
                            <input id="id_organisation_website"
                                   name="organisation_website"
                                   type="url"
                                   class="form-control"
                                   v-model="organisationWebsiteModel"
                            >
                        </div>

                        <!-- ORGANISATION EMAIL -->
                        <div class="form-group col-md-6">
                            <label for="id_organisation_email">
                                Organisation Email:
                                <span class="error"
                                      v-if="!$v.organisationEmailModel.required && $v.organisationEmailModel.$dirty"
                                      > Please supply
                                </span>
                                <span class="error"
                                      v-if="!$v.organisationEmailModel.email && $v.organisationEmailModel.$dirty"
                                      > Please format as Email
                                </span>
                            </label>
                            <input id="id_organisation_email"
                                   name="organisation_email"
                                   type="email"
                                   class="form-control"
                                   v-model="organisationEmailModel"
                            >
                        </div>
                    </div>
                </div>
            </div>
            <hr>

            <!-- SUBMIT ORGANISATION BUTTON -->
            <div class="row submit-row"
                 v-if="duplicateOrganisations.length == 0"
            >
                <div class="col-md-12">
                    <button class="btn btn-primary save-changes"
                            v-on:click="addOrganisation"
                    >
                        Add Organisation
                    </button>
                </div>
            </div>

            <h2 v-if="duplicateOrganisations.length > 0"
            >
                Potential Duplication
            </h2>
            <div class="row"
                 v-if="duplicateOrganisations.length > 0"
            >
                <!-- PLEASE READ -->
                <div class="col-md-4">
                    <strong>Please Read</strong>
                    <p class="text-instructions">
                        The server has found potential duplications. Please review the following Organisations. If you
                        would like to create the organisation, please scroll to the bottom of the page and hit "Submit
                        Organisation". If the organisation you are looking for is already created. Click
                        on the name and you will be taken to the Organisation's Information page.
                    </p>
                    <strong>Alternatively</strong>
                    <p class="text-instructions">
                        You can also change the information above and resubmit.
                    </p>
                </div>
                <!-- DUPLICATE ORGANISATION LIST -->
                <div class="col-md-8">
                    <list-organisations v-bind:organisation-results="duplicateOrganisations"
                    ></list-organisations>
                </div>
            </div>

            <!-- STILL SUBMIT ORGANISATION -->
            <div class="row submit-row" v-if="duplicateOrganisations.length > 0">
                <div class="col-md-12">
                    <button class="btn btn-primary save-changes"
                            v-on:click="uploadOrganisationData"
                    >
                        Submit Organisation
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript Libraries
    const axios = require('axios');
    import { Modal } from 'bootstrap';

    //Validation
    import { email, maxLength, required , url } from 'vuelidate/lib/validators';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    export default {
        name: "NewOrganisation",
        props: [],
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
        data() {
            return {
                duplicateOrganisations: [],
                organisationNameModel: '',
                organisationWebsiteModel: '',
                organisationEmailModel: '',
            }
        },
        watch: {
            organisationNameModel: function() {
                //If user changes anything - reset the duplicate results
                this.duplicateOrganisations = [];
            },
            organisationWebsiteModel: function() {
                //If user changes anything - reset the duplicate results
                this.duplicateOrganisations = [];
            },
            organisationEmailModel: function() {
                //If user changes anything - reset the duplicate results
                this.duplicateOrganisations = [];
            },
        },
        methods: {
            addOrganisation: function() {
                // Check the validation first
                this.$v.$touch();

                if (this.$v.$invalid) {
                    this.showValidationErrorModal();
                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                //Check the organisation's data to make sure there are no duplicates
                //Use axios to contact the database
                axios.post(
                    '/organisation_duplicates/',
                    this.dataToSend(),
                ).then(response => {
                    //If the response data has nothing in it - we want to submit that data.
                    if (response['data'].length == 0) {
                        //Submit that data
                        this.uploadOrganisationData();
                    }

                    //Copy over the response data
                    this.duplicateOrganisations = response['data'];
                }).catch(error => {
                    this.showErrorModal(error,'organisation','')
                })
            },
            dataToSend: function() {
                const data_to_send = new FormData();
                data_to_send.set('organisation_name',this.organisationNameModel);
                data_to_send.set('organisation_website',this.organisationWebsiteModel);
                data_to_send.set('organisation_email',this.organisationEmailModel);

                //Return the data
                return data_to_send;
            },
            uploadOrganisationData: function () {
                //Use Axios to send the data
                //Get the data to send
                axios.post(
                    'save/',
                    this.dataToSend(),
                ).then(response => {
                    //Go to the url sent back
                    window.location.href = response['data'];
                }).catch(error => {
                    console.log("Error: ",error);
                });
            }

        },
        validations: {
            organisationNameModel: {
                required,
                maxLength: maxLength(255),
            },
            organisationWebsiteModel: {
                required,
                url,
            },
            organisationEmailModel: {
                required,
                email,
            },
        },
    }
</script>

<style scoped>

</style>
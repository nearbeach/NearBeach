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
            <div class="row submit-row">
                <div class="col-md-12">
                    <button class="btn btn-primary save-changes"
                        v-on:click="addOrganisation"
                    >
                        Add Organisation
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

    export default {
        name: "NewOrganisation",
        props: [],
        data() {
            return {
                organisationNameModel: '',
                organisationWebsiteModel: '',
                organisationEmailModel: '',
            }
        },
        methods: {
            addOrganisation: function() {
                // Check the validation first
                this.$v.$touch();

                if (this.$v.$invalid) {
                    //Show the error dialog and notify to the user that there were field missing.
                    var elem_cont = document.getElementById("errorModalContent");

                    // Update the content
                    elem_cont.innerHTML =
                        `<strong>FORM ISSUE:</strong> Sorry, but can you please fill out the form completely.`;

                    // Show the modal
                    var errorModal = new Modal(document.getElementById('errorModal'));
                    errorModal.show();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                //Check the organisation's data to make sure there are no duplicates
                const data_to_send = new FormData();
                data_to_send.set('organisation_name',this.organisationNameModel);
                data_to_send.set('organisation_website',this.organisationWebsiteModel);
                data_to_send.set('organisation_email',this.organisationEmailModel);

                //Use axios to contact the database
                axios.post(
                    'organisation_duplicates/',
                    data_to_send,
                ).then(response => {
                    console.log("Response: ",response);
                }).catch(error => {
                    console.log("ERROR");
                })
            },

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
        }
    }
</script>

<style scoped>

</style>
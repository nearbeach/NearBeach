<template>
    <div class="card">
        <div class="card-body">
            <!-- TITLE -->
            <h1>Organisation Information</h1>
            <hr>

            <!-- FIELDS SECTION -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Please Note</strong>
                    <p class="text-instructions">
                        Please only use generic information for both the website and email. Do not use any personal
                        details - you can create contacts in the section below.
                    </p>
                </div>
                <div class="col-md-3">
                    <img v-bind:src="`${staticUrl}/NearBeach/images/placeholder/product_tour.svg`"
                         alt="No Profile Picture"
                         class="organisation-profile-image"
                    />
                    <br/>
                    <button class="btn btn-primary">Update Profile...</button>
                </div>
                <div class="col-md-5">
                    <!-- ORGANISATION NAME -->
                    <div class="form-group">
                        <label for="id_organisation_name">
                            Organisation Name
                            <span class="error"
                                  v-if="!$v.organisationNameModel.required && $v.organisationNameModel.$dirty"
                                > Please suppy a title.
                            </span>
                        </label>
                        <input id="id_organisation_name"
                               v-model="organisationNameModel"
                               type="text"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- ORGANISATION WEBSITE -->
                    <div class="form-group">
                        <label for="id_organisation_website">
                            Organisation Website
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
                               v-model="organisationWebsiteModel"
                               type="text"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- ORGANISATION EMAIL -->
                    <div class="form-group">
                        <label for="id_organisation_email">
                            Organisation Email
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
                               v-model="organisationEmailModel"
                               type="text"
                               class="form-control"
                        >
                    </div>
                </div>
            </div>
            <br/>

            <!-- NEED TO APPLY PERMISSIONS -->
            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateOrganisation"
                    >Update Organisation</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    //VueX
    import { mapGetters } from 'vuex';

    //Validation
    import { email, maxLength, required , url } from 'vuelidate/lib/validators';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    export default {
        name: "OrganisationInformation",
        props: {
            organisationResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            }),
        },
        data() {
            return {
                organisationNameModel: this.organisationResults[0]['fields']['organisation_name'],
                organisationEmailModel: this.organisationResults[0]['fields']['organisation_email'],
                organisationWebsiteModel: this.organisationResults[0]['fields']['organisation_website'],
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
        methods: {
            updateOrganisation: function() {
                //Check validation
                this.$v.$touch();

                if (this.$v.$invalid) {
                    this.showValidationErrorModal();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                //Construct the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('organisation_name',this.organisationNameModel);
                data_to_send.set('organisation_email',this.organisationEmailModel);
                data_to_send.set('organisation_website',this.organisationWebsiteModel);

                //Show the loader
                this.showLoadingModal('Organisation');

                //Use axios to send the data
                axios.post(
                    `${this.rootUrl}organisation_information/${this.organisationResults[0]['pk']}/save/`,
                    data_to_send,
                ).then(response => {
                    this.closeLoadingModal();
                }).catch(error => {
                    this.showErrorModal(error,'organisation',this.organisationResults[0]['pk']);
                })
            },
        }
    }
</script>

<style scoped>

</style>

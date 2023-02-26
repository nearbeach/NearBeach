<template>
    <div class="card">
        <div class="card-body">
            <!-- TITLE -->
            <h1>Organisation Information</h1>
            <br />
            <a v-bind:href="`${rootUrl}search/organisation/`">Back to organisation search</a>
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
                    <img v-bind:src="profilePicture"
                         alt="Profile Picture"
                         class="organisation-profile-image"
                    />
                    <br/>
                    <!--<button class="btn btn-primary">Update Profile...</button>-->
                    <n-upload v-if="userLevel > 1"
                        :action="`${rootUrl}organisation_information/${organisationResults[0].pk}/update_profile/`"
                        :headers="{
                            'X-CSRFTOKEN': getToken('csrftoken'),
                        }"
                        :data="{}"
                        @finish="updateProfilePicture"
                    >
                        <n-button>Update Profile Picture</n-button>
                    </n-upload>
                </div>
                <div class="col-md-5">
                    <!-- ORGANISATION NAME -->
                    <div class="form-group">
                        <label for="id_organisation_name">
                            Organisation Name
                            <span class="error"
                                  v-if="v$.organisationNameModel.$error.length > 0"
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
                                  v-if="v$.organisationWebsiteModel.$error.length > 0"
                                  > Please supply a properly formatted URL
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
                                  v-if="v$.organisationEmailModel.$error.length > 0"
                                  > Please supply a valid Email
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
            <hr v-if="userLevel > 1">
            <div v-if="userLevel > 1"
                 class="row submit-row"
            >
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
    import axios from 'axios';
    //import { NButton, NUpload } from 'naive-ui';
    import { NButton, NUpload } from 'naive-ui';

    //VueX
    import { mapGetters } from 'vuex';

    //Validation
    import useVuelidate from '@vuelidate/core'
    import { email, maxLength, required , url } from '@vuelidate/validators';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";
    import getToken from "../../mixins/getTokenMixin";

    export default {
        name: "OrganisationInformation",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            NButton,
            NUpload,
        },
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
            getToken,
            loadingModalMixin,
        ],
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
                userLevel: "getUserLevel",
            }),
        },
        data() {
            return {
                organisationNameModel: this.organisationResults[0].fields.organisation_name,
                organisationEmailModel: this.organisationResults[0].fields.organisation_email,
                organisationWebsiteModel: this.organisationResults[0].fields.organisation_website,
                profilePicture: "",    
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
            setProfilePicture: function() {
                let profile_picture = this.organisationResults[0].fields.organisation_profile_picture;

                if (profile_picture !== undefined && profile_picture !== null && profile_picture !== "") {
                    //There is a profile image
                    this.profilePicture = `${this.rootUrl}private/${profile_picture}`;
                } else {
                    this.profilePicture = `${this.staticUrl}/NearBeach/images/placeholder/product_tour.svg`
                }
            },
            updateOrganisation: function() {
                //Check validation
                this.v$.$touch();

                if (this.v$.$invalid) {
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
                    `${this.rootUrl}organisation_information/${this.organisationResults[0].pk}/save/`,
                    data_to_send,
                ).then(response => {
                    this.closeLoadingModal();
                }).catch(error => {
                    this.showErrorModal(error,'organisation',this.organisationResults[0].pk);
                })
            },
            updateProfilePicture: function() {
                //Contact the API to get the location of the new image
                axios.post(
                    `${this.rootUrl}organisation_information/${this.organisationResults[0].pk}/get_profile_picture/`,
                    {},
                ).then(response => {
                    this.profilePicture = response.data;
                }).catch(() => {
                    this.profilePicture = `${this.staticUrl}/NearBeach/images/placeholder/product_tour.svg` 
                })
            },
        },
        mounted() {
            //Set profile picture
            this.setProfilePicture();
        }
    }
</script>

<style scoped>

</style>

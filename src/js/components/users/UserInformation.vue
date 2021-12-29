<template>
    <div class="card">
        <div class="card-body">
            <h1>User Information</h1>
            <hr>

            <!-- USERNAME -->
            <div class="row">
                <div class="col-md-4">
                    <strong>UserName</strong>
                    <p class="text-instructions">
                        The username is set and can not be changed from this location. If you need to change the
                        username, please go to the Django Admin Panel.
                    </p>
                    <p class="text-instructions">
                        The ID is the primary key assigned to the username. This can not be edited. It can be ignored.
                    </p>
                </div>
                <div class="col-md-8">
                    <strong>Username:</strong> {{userResults[0]['fields']['username']}}
                    <strong> | ID:</strong> {{userResults[0]['pk']}}
                </div>
            </div>

            <!-- USER DETAILS -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>User Details</strong>
                    <p class="text-instructions">
                        Please fill out the user details.
                    </p>
                </div>
                <div class="col-md-8">
                    <div class="row">
                        <div class="col-md-6">
                            <label>
                              First Name:
                              <span class="error"
                                    v-if="!$v.firstNameModel.required && $v.firstNameModel.$dirty"
                              > Please suppy a first name.</span>
                              <br/>
                            </label>
                            <input type="text"
                                   v-model="firstNameModel"
                                   class="form-control"
                            >
                        </div>
                        <div class="col-md-6">
                            <label>
                              Last Name:
                              <span class="error"
                                    v-if="!$v.lastNameModel.required && $v.lastNameModel.$dirty"
                              > Please suppy a last name.</span>
                              <br/>
                            </label>
                            <input type="text"
                                   v-model="lastNameModel"
                                   class="form-control"
                            >
                        </div>
                        <div class="col-md-6">
                            <label>
                              Email:
                              <span class="error"
                                    v-if="!$v.emailModel.required && $v.emailModel.$dirty"
                              > Please suppy an email.</span>
                              <br/>
                            </label>
                            <input type="email"
                                   v-model="emailModel"
                                   class="form-control"
                            >
                        </div>
                    </div>
                </div>
            </div>
            <hr>

            <!-- Active USER -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Active User</strong>
                    <p class="text-instructions">
                        Untick this option if the user is no longer active.
                    </p>
                </div>
                <div class="col-md-8">
                    <label>Is User Active? </label>
                    <input type="checkbox"
                           v-model="isActiveModel"
                    >
                </div>
            </div>
            <hr>

            <!-- User is SUPER -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Is User a Superuser</strong>
                    <p class="text-instructions">
                        Tick this functionality if you would like the user to gain access to the /admin/ functionality.
                        This is not recommended for anyone outside of an IT team.
                    </p>
                </div>
                <div class="col-md-8">
                    <label>Is User a Superuser? </label>
                    <input type="checkbox"
                           v-model="isSuperuserModel"
                    >
                </div>
            </div>
            <hr>

            <!-- UPDATE USER -->
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateUser"
                    >
                        Update User Details
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    //Import mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    //Validation
    import { required, maxLength, email } from 'vuelidate/lib/validators';

    export default {
        name: "UserInformation",
        props: {
            userResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            rootUrl: {
                type: String,
                default: '/',
            },
        },
        data() {
            return {
                emailModel: this.userResults[0]['fields']['email'],
                isActiveModel: this.userResults[0]['fields']['is_active'],
                isSuperuserModel: this.userResults[0]['fields']['is_superuser'],
                firstNameModel: this.userResults[0]['fields']['first_name'],
                lastNameModel: this.userResults[0]['fields']['last_name'],
            }
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
        validations: {
            lastNameModel: {
                required,
                maxLength: maxLength(255),
            },
            firstNameModel: {
                required,
                maxLength: maxLength(255),
            },
            emailModel: {
                required,
                email,
                maxLength: maxLength(255),
            },
        },
        methods: {
            updateUser: function() {
                //Check form validation
                this.$v.$touch();

                if (this.$v.$invalid) {
                    this.showValidationErrorModal();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                //Start the loading modal
                this.showLoadingModal("User Information")

                //Setup data to send
                const data_to_send = new FormData();
                data_to_send.set('email', this.emailModel);
                data_to_send.set('is_active', this.isActiveModel);
                data_to_send.set('is_superuser', this.isSuperuserModel);
                data_to_send.set('first_name', this.firstNameModel);
                data_to_send.set('last_name', this.lastNameModel);

                axios.post(
                    `${this.rootUrl}user_information/${this.userResults[0]['pk']}/save/`,
                    data_to_send,
                ).then(response => {
                    //Hide the loading modal
                    this.closeLoadingModal();
                }).catch(error => {
                    this.showErrorModal(error, "Update User", this.userResults[0]['pk']);
                });
            },
        },
        mounted() {
            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
            })
        }
    }
</script>

<style scoped>

</style>
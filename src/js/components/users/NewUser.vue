<template>
    <div class="card">
        <div class="card-body">
            <h1>New User</h1>
            <hr>

            <!-- Username -->
            <div class="row">
                <div class="col-md-4">
                    <strong>New User</strong>
                    <p class="text-instructions">
                        Please create a unique username, followed by the basic user details.
                    </p>
                </div>
                <div class="col-md-8">
                    <label>Username: </label>
                    <input type="text"
                           v-model="usernameModel"
                           class="form-control"
                    >
                </div>
            </div>
            <hr>

            <!-- User Details -->
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
                            <label>First Name:</label>
                            <input type="text"
                                   v-model="firstNameModel"
                                   class="form-control"
                            >
                        </div>
                        <div class="col-md-6">
                            <label>Last Name:</label>
                            <input type="text"
                                   v-model="lastNameModel"
                                   class="form-control"
                            >
                        </div>
                        <div class="col-md-6">
                            <label>Email:</label>
                            <input type="email"
                                   v-model="emailModel"
                                   class="form-control"
                            >
                        </div>
                    </div>
                </div>
            </div>
            <hr>

            <!-- User Password -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Passwords</strong>
                    <p class="text-instructions">
                        Please type in a user password. The user will be able to reset their password to log in.
                    </p>
                </div>
                <div class="col-md-8">
                    <div class="row">
                        <div class="col-md-6">
                            <label>Password</label>
                            <input type="password"
                                   v-model="password1Model"
                                   class="form-control"
                            >
                        </div>
                        <div class="col-md-6">
                            <label>Retype Password</label>
                            <input type="password"
                                   v-model="password2Model"
                                   class="form-control"
                            >
                        </div>
                    </div>
                </div>
            </div>

            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="addUser"
                    >
                        Add new User
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

    export default {
        name: "NewUser",
        props: {},
        data() {
            return {
                emailModel: '',
                firstNameModel: '',
                lastNameModel: '',
                password1Model: '',
                password2Model: '',
                usernameModel: '',
            }
        },
        mixins: [
            errorModalMixin,
        ],
        methods: {
            addUser: function() {
                //Setup data to send
                const data_to_send = new FormData();
                data_to_send.set('username', this.usernameModel);
                data_to_send.set('email', this.emailModel);
                data_to_send.set('first_name', this.firstNameModel);
                data_to_send.set('last_name', this.lastNameModel);
                data_to_send.set('password1', this.password1Model);
                data_to_send.set('password2', this.password2Model);

                axios.post(
                    `/new_user/save/`,
                    data_to_send,
                ).then(response => {
                    //Send user to the user information page
                    window.location.href = response['data'];
                }).catch(error => {
                    this.showErrorModal(error, 'New User', '');
                });
            }
        }
    }
</script>

<style scoped>

</style>
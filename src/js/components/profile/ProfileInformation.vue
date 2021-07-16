<template>
    <div class="card">
        <div class="card-body">
            <h1>My Profile</h1>
            <hr>

            <div class="row">
                <div class="col-md-4">
                    <strong>User Details</strong>
                    <p class="text-instructions">
                        Please update your details.
                    </p>
                </div>
                <div class="col-md-8">
                    <p>
                        <strong>Username: </strong>{{userResults[0]['username']}}
                    </p>
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
            <hr/>

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
    import { Modal } from "bootstrap";

    //Validations
    import { required, maxLength } from 'vuelidate/lib/validators';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";
    
    export default {
        name: "ProfileInformation",
        props: {
            userResults: Array,
        },
        data() {
            return {
                emailModel: this.userResults[0]['email'],
                firstNameModel: this.userResults[0]['first_name'],
                lastNameModel: this.userResults[0]['last_name'],
            };
        },
        methods: {
            updateUser: function() {
                //Create data_to_send
                const data_to_send = new FormData();
                data_to_send.set('username', this.userResults[0]['id']);
                data_to_send.set('email', this.emailModel);
                data_to_send.set('first_name', this.firstNameModel);
                data_to_send.set('last_name', this.lastNameModel);

                //Send data via axios
                axios.post(
                    `/profile_information/update_data/`,
                    data_to_send,
                ).then(response => {
                    //ADD CODE
                }).catch(error => {
                    //ADD COD2
                })
            },
        },
    }
</script>

<style>

</style>

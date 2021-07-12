<template>
    <div>
        <div class="card">
            <div class="card-body">
                <h2>Reset Password</h2>
                <hr>

                <!-- PASSWORD -->
                <div class="row">
                    <div class="col-md-4">
                        <strong>Passwords</strong>
                        <p class="text-instructions">
                            Users have the ability to reset their password from the login page. If needed, please click on
                            the link to be taken to the password reset form.
                        </p>
                    </div>
                    <div class="col-md-8">
                        <button type="button" 
                                class="btn btn-warning"
                                v-on:click="passwordResetClicked"
                        >
                            Password Reset
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- PASSWORD RESET MODAL -->
        <div class="modal fade" id="passwordResetModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2><IconifyIcon v-bind:icon="icons.passwordIcon"></IconifyIcon> Reset User Password</h2>
                        <button type="button"
                                class="btn-close"
                                data-bs-dismiss="modal"
                                aria-label="Close"
                                id="passwordResetCloseButton"
                        >
                            <span aria-hidden="true"></span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <label>Password</label>
                                <input type="text"
                                       class="form-control"
                                       v-model="password1Model"
                                >
                            </div>
                            <div class="col-md-6">
                                <label>Confirm Password</label>
                                <input type="text"
                                       class="form-control"
                                       v-model="password2Model"
                                >
                            </div>
                        </div>
                    </div>                   
                    <div class="modal-footer">
                        <button type="button"
                                class="btn btn-secondary"
                                data-bs-dismiss="modal"
                        >Close</button>
                        <button type="button"
                                class="btn btn-primary"
                                v-on:click="updatePassword"
                                v-bind:disabled="disableButton"
                        >Update Password</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript components
    const axios = require('axios');
    import {Modal} from "bootstrap";

    //Mixins
    import errorModalMixin from '../../mixins/errorModalMixin';
    import iconMixin from "../../mixins/iconMixin";

    export default {
        name: "ResetUserPassword",
        props: {},
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        data() {
            return {
                password1Model: '',
                password2Model: '',
            }
        },
        computed: {
            disableButton: function() {
                //Both passwords have to be the same
                let condition_1 = this.password1Model == this.password2Model;

                //Passwords can not be less than 8 character
                let condition_2 = this.password1Model.length >= 8

                return condition_1 && condition_2 == true;
            } 
        },
        methods: {
            passwordResetClicked: function() {
                //Opens the password reset modal
                let passwordResetModal = new Modal(document.getElementById('passwordResetModal'));
                passwordResetModal.show();
            },
            updatePassword: function() {
                
            },
        }
    }
</script>

<style scoped>

</style>

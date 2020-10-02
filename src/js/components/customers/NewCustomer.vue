<template>
    <div class="card">
        <div class="card-body">
            <!-- HEADER -->
            <h1>New Customer</h1>
            <hr>

            <!-- New Customer Form -->
            <new-customer-form v-bind:organisation-name="organisationName"
                               v-bind:title-list="titleList"
                               v-bind:flag-validation-check="flagValidationCheck"
                               v-on:update_customer_data="updateCustomerData($event)"
            ></new-customer-form>

            <!-- REMEMBER TO ADD IN USER PERMISSIONS HERE!! -->
            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="submitNewCustomer"
                    >Submit Customer</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import { Modal } from "bootstrap";

    //Validation
    import { email, required } from 'vuelidate/lib/validators';

    export default {
        name: "NewCustomer",
        props: [
            'organisationName',
            'titleList',
        ],
        data() {
            return {
                customerEmailModel: '',
                customerFirstNameModel: '',
                customerLastNameModel: '',
                flagValidationCheck: false,
                organisationModel: {},
                titleModel: [],
            }
        },
        validations: {
            customerEmailModel: {
                required,
                email,
            },
            customerFirstNameModel: {
                required,
            },
            customerLastNameModel: {
                required,
            },
            titleModel: {
                required,
            },
        },
        methods: {
            submitNewCustomer: function() {
                //Flag downstream to check validation
                this.flagValidationCheck = true;

                //Reset this check after 100ms
                setTimeout(() => {
                    this.flagValidationCheck = false;
                },100);

                // Check the validation at this level
                this.$v.$touch();

                //NEED TO USE MIXIN FOR THIS SECTION
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

                //Create the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('customer_title',this.titleModel['value']);
                data_to_send.set('customer_first_name',this.customerFirstNameModel);
                data_to_send.set('customer_last_name',this.customerLastNameModel);
                data_to_send.set('customer_email',this.customerEmailModel);

                //If there is an organisation in the model - send it
                if (Object.keys(this.organisationModel).length != 0) {
                    data_to_send.set('organisation',this.organisationModel['value']);
                }

                //Send the data using axios
                axios.post(
                    '/new_customer/save/',
                    data_to_send,
                ).then(response => {
                    //Go to the new customer page
                    window.location.href = response['data'];
                }).catch(error => {
                    console.log("Error: ",error);
                })
            },
            updateCustomerData: function(data) {
                //Update the modal field with the value data
                this[data['field']] = data['value'];
            },
        },
    }
</script>

<style scoped>

</style>
<template>
    <div class="card">
        <div class="card-body">
            <!-- TITLE -->
            <h1>Customer Information</h1>
            <hr>

            <!-- FIELDS SECTION -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Please Note</strong>
                    <p class="text-instructions">
                        Please fill out the following details. If the customer is not assigned an organisation,
                        NearBeach will treat this customer as a freelancer.
                    </p>
                </div>
                <div class="col-md-3">
                    <img src="/static/NearBeach/images/placeholder/product_tour.svg"
                         alt="No Profile Picture"
                         class="customer-profile-image"
                    />
                    <br/>
                    <button class="btn btn-primary">Update Profile...</button>
                </div>
                <div class="col-md-5">
                    <div class="form-group col-sm-3">
                        <label>
                            Title:
                            <span class="error"
                                  v-if="!$v.titleModel.required && $v.titleModel.$dirty"
                                  > Please supply
                            </span>
                        </label>
                        <v-select :options="titleFixList"
                                  label="title"
                                  v-model="titleModel"
                        ></v-select>
                    </div>
                    <div class="form-group col-sm-4">
                        <label>
                            First Name:
                            <span class="error"
                                  v-if="!$v.customerFirstNameModel.required && $v.customerFirstNameModel.$dirty"
                                  > Please supply
                            </span>
                        </label>
                        <input type="text"
                               class="form-control"
                               v-model="customerFirstNameModel"
                        >
                    </div>
                    <div class="form-group col-sm-5">
                        <label>
                            Last Name:
                            <span class="error"
                                  v-if="!$v.customerLastNameModel.required && $v.customerLastNameModel.$dirty"
                                  > Please supply
                            </span>
                        </label>
                        <input type="text"
                               class="form-control"
                               v-model="customerLastNameModel"
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
                       v-on:click="updateCustomer"
                    >Update Customer</a>
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
        name: "CustomerInformation",
        props: [
            'customerResults',
            'titleList',
        ],
        data() {
            return {
                customerEmailModel: this.customerResults[0]['fields']['customer_email'],
                customerFirstNameModel: this.customerResults[0]['fields']['customer_first_name'],
                customerLastNameModel: this.customerResults[0]['fields']['customer_last_name'],
                customerTitleModel: this.customerResults[0]['fields']['customer_title'],
                titleFixList: [],
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
            organisationModel: {
                required,
            },
            titleModel: {
                required,
            },
        },
        methods: {
            updateCustomer: function() {
                //Construct the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('customer_email',this.customerEmailModel);
                data_to_send.set('customer_first_name',this.customerFirstNameModel);
                data_to_send.set('customer_last_name',this.customerLastNameModel);
                data_to_send.set('customer_title',this.customerTitleModel);

                //Use axios to send the data
                axios.post(
                    `/customer_information/${this.customerResults[0]['pk']}/save/`,
                    data_to_send,
                ).then(response => {
                    console.log("Response: ",response);
                }).catch(error => {
                    console.log("Error: ",error);
                })
            },
        },
        mounted() {
            //Get the title list data and convert it so the v-select can use it
            this.titleList.forEach(row => {
                this.titleFixList.push({
                    'value': row['pk'],
                    'title': row['fields']['title'],
                });
            });
        }
    }
</script>

<style scoped>

</style>
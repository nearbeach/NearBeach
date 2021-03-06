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
                <div class="col-md-8">
                    <div class="row customer-profile-image">
                        <!-- PROFILE IMAGE -->
                        <img src="/static/NearBeach/images/placeholder/product_tour.svg"
                             alt="No Profile Picture"
                             class="customer-profile-image"
                        />
                        <br/>
                        <button class="btn btn-primary">Update Profile...</button>
                    </div>
                    <br/>

                    <!-- CUSTOMER INFORMATION -->
                    <div class="row">
                        <div class="form-group col-sm-3">
                            <label>
                                Title:
                                <span class="error"
                                      v-if="!$v.customerTitleModel.required && $v.customerTitleModel.$dirty"
                                      > Please supply
                                </span>
                            </label>
                            <v-select :options="titleFixList"
                                      label="title"
                                      v-model="customerTitleModel"
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
            </div>
            <!-- STAKEHOLDER ORGANISATION -->
            <hr>
            <stakeholder-information v-bind:organisation-results="organisationResults"
                                     v-bind:default-stakeholder-image="defaultStakeholderImage"
                                     v-if="organisationResults.length>0"
            ></stakeholder-information>

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

    //Import Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    export default {
        name: "CustomerInformation",
        props: {
            customerResults: Array,
            defaultStakeholderImage: String,
            organisationResults: Array,
            titleList: Array,
        },
        data() {
            return {
                customerEmailModel: this.customerResults[0]['fields']['customer_email'],
                customerFirstNameModel: this.customerResults[0]['fields']['customer_first_name'],
                customerLastNameModel: this.customerResults[0]['fields']['customer_last_name'],
                customerTitleModel: this.customerResults[0]['fields']['customer_title'],
                titleFixList: [],
            }
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
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
            customerTitleModel: {
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
                data_to_send.set('customer_title',this.customerTitleModel['value']);

                //Show loading screen
                this.showLoadingModal('Customer Information');

                //Use axios to send the data
                axios.post(
                    `/customer_information/${this.customerResults[0]['pk']}/save/`,
                    data_to_send,
                ).then(response => {
                    //Close the loading screen
                    this.closeLoadingModal();
                }).catch(error => {
                    //Show the error modal
                    this.showErrorModal(error, 'customer',this.customerResults[0]['pk']);
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

                //If the primary key is the same as the customerTitleModel - update customerTitleModel with this object
                if (row['pk'] == this.customerTitleModel) {
                    this.customerTitleModel = {
                        'value': row['pk'],
                        'title': row['fields']['title'],
                    }
                }
            });
        }
    }
</script>

<style scoped>

</style>
<template>
    <div class="row">
        <div class="col-md-4">
            <strong>New Customer</strong>
            <p class="text-instructions">
                Please fill out the following details.
            </p>
            <strong>Please Note:</strong>
            <p class="text-instructions">
                Customers do not go through a duplication process. Please search for the potential customer
                first before adding them into NearBeach.
            </p>
        </div>
        <div class="col-md-8">
            <!-- CUSTOMER DETAILS -->
            <div class="row">
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
            <br/>

            <!-- Customer Email -->
            <div class="form-group col-sm-8">
                <label>
                    Email:
                    <span class="error"
                          v-if="!$v.customerEmailModel.required && $v.customerEmailModel.$dirty"
                          > Please supply
                    </span>
                    <span class="error"
                          v-if="!$v.customerEmailModel.email && $v.customerEmailModel.$dirty"
                          > Please format as Email
                    </span>
                </label>
                <input type="text"
                       class="form-control"
                       v-model="customerEmailModel"
                >
            </div>
            <br/>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import { Modal } from "bootstrap";

    //Validation
    import { email, required } from 'vuelidate/lib/validators';

    export default {
        name: "NewCustomerForm",
        props: [
            'flagValidationCheck',
            'organisationName',
            'titleList',
        ],
        data() {
            return {
                customerEmailModel: '',
                customerFirstNameModel: '',
                customerLastNameModel: '',
                organisationModel: {},
                searchTimeout: '',
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

        },
        watch: {
            customerEmailModel: function() {
                //Emit up this function's data
                this.$emit(
                    'update_customer_data',
                    {
                        'field': 'customerEmailModel',
                        'value': this.customerEmailModel,
                    }
                )
            },
            customerFirstNameModel: function() {
                //Emit up this function's data
                this.$emit(
                    'update_customer_data',
                    {
                        'field': 'customerFirstNameModel',
                        'value': this.customerFirstNameModel,
                    }
                )
            },
            customerLastNameModel: function() {
                //Emit up this function's data
                this.$emit(
                    'update_customer_data',
                    {
                        'field': 'customerLastNameModel',
                        'value': this.customerLastNameModel,
                    }
                )
            },
            flagValidationCheck: function() {
                //Don't worry if it is false
                if (!this.flagValidationCheck) return;

                //Touch the validation
                this.$v.$touch();
            },
            // organisationModel: function() {
            //     //Emit up this function's data
            //     this.$emit(
            //         'update_customer_data',
            //         {
            //             'field': 'organisationModel',
            //             'value': this.organisationModel
            //         }
            //     )
            // },
            titleModel: function() {
                //Emit up this function's data
                this.$emit(
                    'update_customer_data',
                    {
                        'field': 'titleModel',
                        'value': this.titleModel,
                    }
                )
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
        },
    }
</script>

<style scoped>

</style>
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
                              v-if="v$.titleModel.$error"
                              > Please supply
                        </span>
                    </label>
                    <n-select :options="titleFixList"
                              label="title"
                              placeholder=""
                              v-model:value="titleModel"
                    ></n-select>
                </div>
                <div class="form-group col-sm-4">
                    <label>
                        First Name:
                        <span class="error"
                              v-if="v$.customerFirstNameModel.$error"
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
                              v-if="v$.customerLastNameModel.$error"
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
                          v-if="v$.customerEmailModel.$error"
                          > Please supply
                    </span>
                    <span class="error"
                          v-if="v$.customerEmailModel.$error"
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
    import { NSelect } from 'naive-ui';

    //Validation
    import useVuelidate from '@vuelidate/core'
    import { required, email } from '@vuelidate/validators'

    export default {
        name: "NewCustomerForm",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            NSelect,
        },
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
                
                this.v$.$touch();
                
            },
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
            //Get the data formatted how the NSelect wants
            this.titleFixList = this.titleList.map(row => {
                return {
                    value: row['pk'],
                    label: row['fields']['title'],
                }
            });
        },
    }
</script>

<style scoped>

</style>

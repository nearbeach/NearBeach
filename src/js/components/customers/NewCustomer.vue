<template>
    <div class="card">
        <div class="card-body">
            <!-- HEADER -->
            <h1>New Customer</h1>
            <hr>

            <!-- ROW -->
            <div class="row">
                <div class="col-md-4">
                    <strong>New Customer</strong>
                    <p class="text-instructions">
                        Please fill out the following details. If the customer is not assigned an organisation,
                        NearBeach will treat this customer as a freelancer.
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
                               @search="fetchOptions"
                        >
                    </div>
                    <br/>

                    <!-- CUSTOMER ORGANISATION -->
                    <div class="form-group col-sm-8">
                        <label>Organisation:</label>
                        <v-select :options="organisationFixList"
                          @search="fetchOptions"
                          v-model="organisationModel"
                          label="organisation_name"
                          class="get-stakeholders"
                        ></v-select>
                    </div>
                </div>
            </div>

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
                organisationFixList: [],
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
            fetchOptions: function(search, loading) {
                // Make sure the timer isn't running
                if (this.searchTimeout != '') {
                    //Stop the clock!
                    clearTimeout(this.searchTimeout);
                }

                // Reset the clock, to only search if there is an uninterupted 0.5s of no typing.
                if (search.length >= 3) {
                    this.searchTimeout = setTimeout(
                        this.getOrganisationData,
                        500,
                        search,
                        loading
                    )
                }
            },
            getOrganisationData: function(search,loading) {
                // Save the seach data in FormData
                const data_to_send = new FormData();
                data_to_send.set('search',search);

                // Now that the timer has run out, lets use AJAX to get the organisations.
                axios.post(
                    '/search/organisation/data/',
                    data_to_send
                ).then(response => {
                    //Clear the stakeholderFixList
                    this.organisationFixList = [];

                    //Extract the required JSON data
                    var extracted_data = response['data'];

                    //Look through the extracted data - and map the required fields into stakeholder fix list
                    extracted_data.forEach((row) => {
                        //Create the creation object
                        var creation_object = {
                            'value': row['pk'],
                            'organisation_name': row['fields']['organisation_name'],
                            'organisation_website': row['fields']['organisation_website'],
                            'organisation_email': row['fields']['organisation_email'],
                            'organisation_profile_picture': row['fields']['organisation_profile_picture'],
                        };

                        //Push that object into the stakeholders
                        this.organisationFixList.push(creation_object)
                    });

                    //If there is an organisation Name - we want to filter it out of the results and place it into
                    //the modal
                    var filtered_results = this.organisationFixList.filter(row => {
                        return row['organisation_name'] == this.organisationName;
                    });
                    if (filtered_results.length > 0) {
                        //Get the first value - which should be the proper organisation
                        this.organisationModel = filtered_results[0];
                    }
                }).catch(function (error) {
                    // Get the error modal
                    var elem_cont = document.getElementById("errorModalContent");

                    // Update the content
                    elem_cont.innerHTML = `<strong>Search Organisation Issue:</strong><br/>${error}`;

                    // Show the modal
                    var errorModal = new Modal(document.getElementById('errorModal'), {
                      keyboard: false
                    })
                    errorModal.show();

                    // Hide the loader
                    var loader_element = document.getElementById("loader");
                    loader_element.style.display = "none";
                });
            },
            submitNewCustomer: function() {
                                // Check the validation first
                this.$v.$touch();

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
            }
        },
        mounted() {
            //Get the title list data and convert it so the v-select can use it
            this.titleList.forEach(row => {
                this.titleFixList.push({
                    'value': row['pk'],
                    'title': row['fields']['title'],
                });
            });

            //If there is a value in organisation name - search for it
            if (this.organisationName != '') {
                this.getOrganisationData(this.organisationName,null)
            }
        },
    }
</script>

<style scoped>

</style>
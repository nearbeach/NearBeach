<template>
    <div>
        <h2><i data-feather="users"></i> Customers</h2>
        <p class="text-instructions">
            Below are a list of customers who are stakeholders to this {{destination}}.
        </p>

        <!-- CUSTOMER RESULTS CARDS -->
        <div v-if="customerResults.length == 0">
            <div class="customers-module-spacer">
                <div class="alert alert-dark">
                    Sorry - there are no customers. Please add them by clicking on the button below
                </div>
            </div>
        </div>
        <div v-else
             class="customer-modules"
        >
            <div v-for="customer in customerResults"
                 class="card card-customer"
            >
                <div class="card-body">
                    <div class="single-customer-card">
                        <img v-bind:src="getCustomerImage(customer)" alt="default profile picture" />
                        <div class="customer-card-name">
                            {{customer['fields']['customer_first_name']}} {{customer['fields']['customer_last_name']}}
                        </div>
                        <div class="customer-card-email"><i data-feather="email"></i>
                            {{customer['fields']['customer_email']}}
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <!-- ADD CUSTOMER BUTTON -->
        <hr>
        <div class="row submit-row">
            <div class="col-md-12">
                <button class="btn btn-primary save-changes"
                        v-on:click="addNewCustomer"
                >
                    Add Customer
                </button>
            </div>
        </div>

        <!-- MODALS -->
        <new-customer-wizard v-bind:location-id="locationId"
                             v-bind:destination="destination"
                             v-bind:exclude-customers="customerResults"
                             v-on:update_customer_results="updateCustomerResults($event)"
        ></new-customer-wizard>
    </div>
</template>

<script>
    //JavaScript components
    const axios = require('axios');
    import {Modal} from "bootstrap";

    export default {
        name: "CustomersModule",
        props: [
            'destination',
            'locationId',
        ],
        data() {
            return {
                customerResults: [],
                defaultCustomerImage: '/static/NearBeach/images/placeholder/people_tax.svg',
            }
        },
        methods: {
            addNewCustomer: function() {
                var addCustomerModal = new Modal(document.getElementById('addCustomerModal'));
                    addCustomerModal.show();
            },
            getCustomerImage: function(customer) {
                if (customer['fields']['customer_profile_picture'] == '') {
                    //There is no image - return the default image
                    return this.defaultCustomerImage;
                }
                return customer['customer_profile_picture'];
            },
            loadCustomerResults: function() {
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/customer_list/`,
                ).then((response) => {
                    this.customerResults = response['data'];
                }).catch((error) => {
                    console.log("ERROR: ",error);
                })
            },
            updateCustomerResults: function(data) {
                this.customerResults = data;
            },
        },
        mounted() {
            this.loadCustomerResults();
        }
    }
</script>

<style scoped>

</style>
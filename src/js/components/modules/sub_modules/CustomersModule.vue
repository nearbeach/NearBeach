<template>
    <div>
        <h2><Icon v-bind:icon="icons.userIcon"></Icon> Customers</h2>
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
        <div v-else>
            <customers-list-module v-bind:customer-results="customerResults"
            ></customers-list-module>
        </div>


        <!-- ADD CUSTOMER BUTTON -->
        <hr>
        <div class="row submit-row">
            <div class="col-md-12">
                <button class="btn btn-primary save-changes"
                        v-on:click="addNewCustomer"
                        v-if="userLevel > 1"
                >
                    Add Customer
                </button>
            </div>
        </div>

        <!-- MODALS -->
        <add-customer-wizard v-bind:location-id="locationId"
                             v-bind:destination="destination"
                             v-bind:exclude-customers="customerResults"
                             v-on:update_customer_results="updateCustomerResults($event)"
        ></add-customer-wizard>
    </div>
</template>

<script>
    //JavaScript components
    import errorModalMixin from "../../../mixins/errorModalMixin";
    import iconMixin from "../../../mixins/iconMixin";
    import { Icon } from '@iconify/vue';

    //VueX
    import { mapGetters } from 'vuex';

    const axios = require('axios');
    import {Modal} from "bootstrap";

    export default {
        name: "CustomersModule",
        components: {
            Icon,
        },
        props: {
            destination: {
                type: String,
                default: "",
            },
            locationId: {
                type: Number,
                default: 0,
            },
        },
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        data() {
            return {
                customerResults: [],
            }
        },
        computed: {
            ...mapGetters({
                userLevel: "getUserLevel",
                rootUrl: "getRootUrl",
            })
        },
        methods: {
            addNewCustomer: function() {
                var addCustomerModal = new Modal(document.getElementById('addCustomerModal'));
                    addCustomerModal.show();
            },
            loadCustomerResults: function() {
                axios.post(
                    `${this.rootUrl}object_data/${this.destination}/${this.locationId}/customer_list/`,
                ).then((response) => {
                    this.customerResults = response['data'];
                }).catch((error) => {
                    this.showErrorModal(error, this.destination);
                })
            },
            updateCustomerResults: function(data) {
                this.customerResults = data;
            },
        },
        mounted() {
            //Wait 200ms before getting data
            setTimeout(() => {
                this.loadCustomerResults();
            }, 200);
        }
    }
</script>

<style scoped>

</style>

<template>
    <div class="modal fade" id="addCustomerModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="users"></i> Add Customers Wizard</h2>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Select Customer</strong>
                            <p class="text-instructions">
                                Search for a customer who has not been added to this {{destination}}. If the search is
                                blank there are either no customers that match that search, or all customer have already
                                been added to the {{destination}}.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <v-select :options="customerList"
                                label="customerName"
                                v-model="customerModel"
                            ></v-select>
                        </div>
                    </div>

                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" v-bind:diabled="customerModel == ''">Save changes</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript components
    const axios = require('axios');

    export default {
        name: "NewCustomerWizard",
        props: [],
        data() {
            return {
                customerModel: '',
                customerList: [],
            }
        },
        methods: {
            getCustomerList: function() {

            }
        }
    }
</script>

<style scoped>

</style>
<template>
    <div class="card">
        <div class="card-body">
            <ul class="nav nav-tabs" id="misc_module_tabs" role="tablist">
                <!-- RISK -->
                <li class="nav-item"
                    role="presentation"
                >
                    <button class="nav-link"
                            id="rfc-risk-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#rfc-risk"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="true"
                    >Risk</button>
                </li>

                <!-- IMPLEMENTATION -->
                <li class="nav-item"
                    role="presentation"
                >
                    <button class="nav-link"
                            id="rfc-implementation-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#rfc-implementation"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="true"
                    >Implementation</button>
                </li>

                <!-- BACKOUT PLAN -->
                <li class="nav-item"
                    role="presentation"
                >
                    <button class="nav-link"
                            id="rfc-backout-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#rfc-backout"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="true"
                    >Backout Plan</button>
                </li>

                <!-- TEST PLAN -->
                <li class="nav-item"
                    role="presentation"
                >
                    <button class="nav-link"
                            id="rfc-test-plan-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#rfc-test"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="true"
                    >Test Plan</button>
                </li>

                <!-- RUN SHEET -->
                <li class="nav-item"
                    role="presentation"
                >
                    <button class="nav-link"
                            id="rfc-run-sheet-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#rfc-run-sheet"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="true"
                    >Run Sheet</button>
                </li>
            </ul>
            <hr>

            <div class="tab-content" id="misc_module_content">
                <div class="tab-pane fade"
                     id="rfc-risk"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    <rfc-risk v-bind:rfc-results="rfcResults"
                              v-bind:is-read-only="isReadOnly"
                              v-on:update_validation="updateValidation($event)"
                              v-on:update_values="updateValues($event)"
                    ></rfc-risk>

                    <!-- Update Button -->
                    <hr v-if="!isReadOnly">
                    <div class="row submit-row"
                         v-if="!isReadOnly"
                    >
                        <div class="col-md-12">
                            <a href="javascript:void(0)"
                               class="btn btn-primary save-changes"
                               v-on:click="updateRisk"
                            >Update Risks</a>
                        </div>
                    </div>
                </div>

                <div class="tab-pane fade"
                     id="rfc-implementation"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    <rfc-implementation-plan v-bind:rfc-results="rfcResults"
                                             v-bind:is-read-only="isReadOnly"
                                             v-on:update_validation="updateValidation($event)"
                                             v-on:update_values="updateValues($event)"
                    ></rfc-implementation-plan>

                    <!-- Update Button -->
                    <hr v-if="!isReadOnly">
                    <div class="row submit-row"
                         v-if="!isReadOnly"
                    >
                        <div class="col-md-12">
                            <a href="javascript:void(0)"
                               class="btn btn-primary save-changes"
                               v-on:click="updateImplementation"
                            >Update Implementation Plan</a>
                        </div>
                    </div>
                </div>

                <div class="tab-pane fade"
                     id="rfc-backout"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    <rfc-backout-plan v-bind:rfc-results="rfcResults"
                                      v-bind:is-read-only="isReadOnly"
                                      v-on:update_validation="updateValidation($event)"
                                      v-on:update_values="updateValues($event)"
                    ></rfc-backout-plan>

                    <!-- Update Button -->
                    <hr v-if="!isReadOnly">
                    <div class="row submit-row"
                         v-if="!isReadOnly"
                    >
                        <div class="col-md-12">
                            <a href="javascript:void(0)"
                               class="btn btn-primary save-changes"
                               v-on:click="updateBackoutPlan"
                            >Update Backout Plan</a>
                        </div>
                    </div>
                </div>

                <div class="tab-pane fade"
                     id="rfc-test"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    <rfc-test-plan v-bind:rfc-results="rfcResults"
                                   v-bind:is-read-only="isReadOnly"
                                   v-on:update_validation="updateValidation($event)"
                                   v-on:update_values="updateValues($event)"
                    ></rfc-test-plan>

                    <!-- Update Button -->
                    <hr v-if="!isReadOnly">
                    <div class="row submit-row"
                         v-if="!isReadOnly"
                    >
                        <div class="col-md-12">
                            <a href="javascript:void(0)"
                               class="btn btn-primary save-changes"
                               v-on:click="updateTestPlan"
                            >Update Test Plan</a>
                        </div>
                    </div>
                </div>

                <div class="tab-pane fade"
                     id="rfc-run-sheet"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    <rfc-run-sheet-list v-bind:is-read-only="isReadOnly"
                                        v-bind:location-id="locationId" 
                                        v-bind:user-list="userList"
                                        v-bind:rfc-id="rfcResults[0]['pk']"
                                        v-bind:rfc-status="rfcResults[0]['fields']['rfc_status']"
                                        v-on:update_values="updateValues($event)"
                    ></rfc-run-sheet-list>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    export default {
        name: "RfcModules",
        props: {
            locationId: Number,
            destination: String,
            isReadOnly: {
                type: Boolean,
                default: false,
            },
            rfcResults: {
                type: Array,
                default: [],
            },
            userList: Array,
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
        data: () => ({
            rfcData: {
                'rfcBackoutPlan': '',
                'rfcImpactModel': {},
                'rfcImplementationPlanModel': '',
                'rfcPriorityModel': {},
                'rfcRiskModel': {},
                'rfcRiskSummaryModel': '',
                'rfcTestPlanModel': '',
                'rfcTypeModel': {},
            },
            validationData: {
                'tab_2': true,
                'tab_3': true,
                'tab_4': true,
                'tab_5': true,
            }
        }),
        methods: {
            sendData: function(data_to_send,url) {
                //Open up the loading modal
                this.showLoadingModal('Project');

                //Use axios to send the data
                axios.post(
                    url,
                    data_to_send,
                ).then(response => {
                    //Notify user of success update
                    this.closeLoadingModal();
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })
            },
            updateBackoutPlan: function() {
                if (this.validationData['tab_4'] === false) {
                    //The data isn't valid. Notify the user, and do nothing else
                    this.showErrorModal("Please fill out all data","Backout Plan","");

                    //Doing nothing else
                    return;
                }

                const data_to_send = new FormData();
                data_to_send.set('text_input', this.rfcData['rfcBackoutPlan']);

                //Send data
                this.sendData(data_to_send, `/rfc_information/${this.rfcResults[0]['pk']}/save/backout/`)
            },
            updateImplementation: function() {
                if (this.validationData['tab_3'] === false) {
                    //The data isn't valid. Notify the user, and do nothing else
                    this.showErrorModal("Please fill out all data","Implementation","");

                    //Doing nothing else
                    return;
                }

                const data_to_send = new FormData();
                data_to_send.set('text_input', this.rfcData['rfcImplementationPlanModel']);
                
                //Send data
                this.sendData(data_to_send, `/rfc_information/${this.rfcResults[0]['pk']}/save/implementation/`);
            },
            updateRisk: function() {
                if (this.validationData['tab_2'] === false) {
                    //The data isn't valid. Notify the user, and do nothing else
                    this.showErrorModal("Please fill out all data","Risk","");

                    //Doing nothing else
                    return;
                }

                //Create the data to send
                const data_to_send = new FormData();
                data_to_send.set('priority_of_change', this.rfcData['rfcPriorityModel']['value']);
                data_to_send.set('risk_of_change', this.rfcData['rfcRiskModel']['value']);
                data_to_send.set('impact_of_change', this.rfcData['rfcImpactModel']['value']);
                data_to_send.set('text_input', this.rfcData['rfcRiskSummaryModel']);

                //Send the data
                this.sendData(data_to_send, `/rfc_information/${this.rfcResults[0]['pk']}/save/risk/`)
            },
            updateValidation: function(data) {
                //Update the value
                this.validationData[data['tab']] = data['value'];
            },
            updateTestPlan: function() {
                if (this.validationData['tab_5'] === false) {
                    //The data isn't valid. Notify the user, and do nothing else
                    this.showErrorModal("Please fill out all data","Test Plan","");

                    //Doing nothing else
                    return;
                }

                const data_to_send = new FormData();
                data_to_send.set('text_input', this.rfcData['rfcTestPlanModel']);

                //Send data
                this.sendData(data_to_send, `/rfc_information/${this.rfcResults[0]['pk']}/save/test/`);
            },
            updateValues: function(data) {
                //Update the value
                this.rfcData[data['modelName']] = data['modelValue'];
            }
        }
    }
</script>

<style scoped>

</style>

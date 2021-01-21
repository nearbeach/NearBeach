<template>
    <div class="card">
        <div class="card-body">
            <ul class="nav nav-tabs" id="misc_module_tabs" role="tablist">
                <!-- RISK -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-risk-tab"
                       data-toggle="tab"
                       href="#rfc-risk"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Risk</a>
                </li>

                <!-- IMPLEMENTATION -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-implementation-tab"
                       data-toggle="tab"
                       href="#rfc-implementation"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Implementation</a>
                </li>

                <!-- BACKOUT PLAN -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-backout-tab"
                       data-toggle="tab"
                       href="#rfc-backout"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Backout Plan</a>
                </li>

                <!-- TEST PLAN -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-test-plan-tab"
                       data-toggle="tab"
                       href="#rfc-test"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Test Plan</a>
                </li>

                <!-- RUN SHEET -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-run-sheet-tab"
                       data-toggle="tab"
                       href="#rfc-run-sheet"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Run Sheet</a>
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
        }),
        methods: {
            updateBackoutPlan: function() {
                const data_to_send = new FormData();
                data_to_send.set('text_input',this.rfcData['rfcBackoutPlan']);

                axios.post(
                    `/rfc_information/${this.rfcResults[0]['pk']}/save/backout_plan/`,
                    data_to_send,
                ).then(response => {
                    //ADD CODE TO TELL USER YAY DID IT!
                }).catch(error => {
                    //CODE IN MIXIN STUFF :D
                })
            },
            updateImplementation: function() {},
            updateRisk: function() {
                //Create the data to send
                const data_to_send = new FormData();
                data_to_send.set('rfc_priority', this.rfcData['rfcPriorityModel']['value']);
                data_to_send.set('rfc_risk', this.rfcData['rfcRiskModel']['value']);
                data_to_send.set('rfc_impact', this.rfcData['rfcImpactModel']['value']);
                data_to_send.set('rfc_risk_and_impact_analysis', this.rfcData['rfcRiskSummaryModel']);

                //Open up the loading modal
                this.showLoadingModal('Project');
                
                //Use axios to send the data
                axios.post(
                    `/rfc_information/${this.rfcResults[0]['pk']}/save/risk/`,
                    data_to_send,
                ).then(response => {
                    //Notify user of success update
                    this.closeLoadingModal();
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })
            },
            updateTestPlan: function() {},
            updateValues: function(data) {
                //Update the value
                this.rfcData[data['modelName']] = data['modelValue'];
            }
        }
    }
</script>

<style scoped>

</style>

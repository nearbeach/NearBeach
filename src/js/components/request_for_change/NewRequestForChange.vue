<template>
    <div class="card">
        <div class="card-body">
            <h1>New Request for Change</h1>
            <hr>

            <!-- FORM WIZARD -->
            <form-wizard @on-complete="onComplete"
                         @on-change="onChange($event)"
                         title=""
                         subtitle=""
            >
                <!-- Description -->
                <tab-content title="Description">
                    <rfc-description v-on:update_values="updateValues($event)"></rfc-description>
                </tab-content>

                <!-- Details -->
                <tab-content title="Details">
                    <rfc-details v-bind:group-results="groupResults"
                                 v-bind:user-results="userResults"
                                 v-on:update_values="updateValues($event)"
                    ></rfc-details>
                </tab-content>

                <!-- Risk -->
                <tab-content title="Risk">
                    <rfc-risk v-on:update_values="updateValues($event)"></rfc-risk>
                </tab-content>

                <!-- Implementation Plan -->
                <tab-content title="Implementation Plan">
                    <rfc-implementation-plan v-on:update_values="updateValues($event)"></rfc-implementation-plan>
                </tab-content>

                <!-- Backout Plan -->
                <tab-content title="Backout Plan">
                    <rfc-backout-plan v-on:update_values="updateValues($event)"></rfc-backout-plan>
                </tab-content>

                <!-- Test Plan -->
                <tab-content title="Test Plan">
                    <rfc-test-plan v-on:update_values="updateValues($event)"></rfc-test-plan>
                </tab-content>
            </form-wizard>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    import {FormWizard, TabContent} from 'vue-form-wizard'
    import 'vue-form-wizard/dist/vue-form-wizard.min.css'

    // Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    export default {
        name: "NewRequestForChange",
        components: {
            FormWizard,
            TabContent
        },
        props: {
            groupResults: Array,
            userResults: Array,
        },
        mixins: [
            errorModalMixin,
        ],
        data: () => ({
            rfcData: {
                'groupModel': [],
                'rfcBackoutPlan': '',
                'rfcChangeLeadModel': {},
                'rfcImpactModel': {},
                'rfcImplementationEndModel': '',
                'rfcImplementationPlanModel': '',
                'rfcImplementationStartModel': '',
                'rfcPriorityModel': {},
                'rfcReleaseModel': '',
                'rfcRiskModel': {},
                'rfcRiskSummaryModel': '',
                'rfcSummaryModel': '',
                'rfcTestPlanModel': '',
                'rfcTitleModel': '',
                'rfcTypeModel': {},
                'rfcVersionModel': '',
            },
        }),
        methods: {
            onChange: function(prevIndex,nextIndex) {
                console.log("Prev Index: ",prevIndex," | Next Index: ",nextIndex);
            },
            onComplete: function() {
                // Setup the new data form
                const data_to_send = new FormData();
                const data = this.rfcData;

                data_to_send.set('rfc_title', data.rfcTitleModel);
                data_to_send.set('rfc_summary', data.rfcSummaryModel);
                data_to_send.set('rfc_type', data.rfcTypeModel['value']);
                data_to_send.set('rfc_implementation_start_date', data.rfcImplementationStartModel);
                data_to_send.set('rfc_implementation_end_date', data.rfcImplementationEndModel);
                data_to_send.set('rfc_implementation_release_date', data.rfcReleaseModel);
                data_to_send.set('rfc_version_number', data.rfcVersionModel);
                data_to_send.set('rfc_lead', data.rfcChangeLeadModel['value']);
                data_to_send.set('rfc_priority', data.rfcPriorityModel['value']);
                data_to_send.set('rfc_risk', data.rfcRiskModel['value']);
                data_to_send.set('rfc_impact', data.rfcImpactModel['value']);
                data_to_send.set('rfc_risk_and_impact_analysis', data.rfcRiskSummaryModel);
                data_to_send.set('rfc_implementation_plan', data.rfcImplementationPlanModel);
                data_to_send.set('rfc_backout_plan', data.rfcBackoutPlan);
                data_to_send.set('rfc_test_plan', data.rfcTestPlanModel);

                // Insert a new row for each group list item
                data.groupModel.forEach((row,index) => {
                    data_to_send.append(`group_list`,row['value']);
                });

                axios.post(
                    `/new_request_for_change/save/`,
                    data_to_send,
                ).then(response => {
                    // Just go to the location the data sent back
                    window.location.href = response['data'];
                }).catch(error => {
                    this.showErrorModal(error,'request_for_change','')
                });
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
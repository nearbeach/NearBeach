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
    import {FormWizard, TabContent} from 'vue-form-wizard'
    import 'vue-form-wizard/dist/vue-form-wizard.min.css'

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
        data: () => ({
            rfcData: {
                'groupModel': [],
                'rfcBackoutPlan': '',
                'rfcChangeLead': {},
                'rfcImpaceModel': {},
                'rfcImplementationEndModel': '',
                'rfcImplementationPlanModel': '',
                'rfcImplementationStartModel': '',
                'rfcPriorityModel': {},
                'rfcReleaseModel': '',
                'rfcRiskModel': {},
                'rfcSummaryModel': '',
                'rfcTestPlan': '',
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
                console.log("Need to send this data: ",this.rfcData);
                //ADD CODE
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
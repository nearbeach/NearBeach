<template>
    <div class="row">
        <div class="col-md-4">
            <h2>Risk</h2>
            <p class="text-instructions">
                Please outline all risks associated with this Request for Change. A detail list of all risks should be
                noted.
            </p>
        </div>

        <div class="col-md-8" style="min-height: 610px;">
            <div class="row">
                <div class="col-md-4">
                    <label>
                        Priority of Change
                        <span class="error" v-if="!v$.rfcPriorityModel.required && v$.rfcPriorityModel.$dirty"
                        > Please select a Change Type.</span>
                    </label>
                    <v-select v-bind:options="rfcPriority"
                              v-bind:disabled="isReadOnly"
                              v-model="rfcPriorityModel"
                    ></v-select>
                </div>
                <div class="col-md-4">
                    <label>
                        Risk of Change
                        <span class="error" v-if="!v$.rfcRiskModel.required && v$.rfcRiskModel.$dirty"
                        > Please select a Change Type.</span>
                    </label>
                    <v-select v-bind:options="rfcRisk"
                              v-bind:disabled="isReadOnly"
                              v-model="rfcRiskModel"
                    ></v-select>
                </div>
                <div class="col-md-4">
                    <label>
                        Impact of Change
                        <span class="error" v-if="!v$.rfcImpactModel.required && v$.rfcImpactModel.$dirty"
                        > Please select a Change Type.</span>
                    </label>
                    <v-select v-bind:options="rfcImpact"
                              v-bind:disabled="isReadOnly"
                              v-model="rfcImpactModel"
                    ></v-select>
                </div>
            </div>
            <br/>

            <!-- RFC SUMMARY -->
            <label>Risk Association:
                <span class="error" v-if="!v$.rfcRiskSummaryModel.required && v$.rfcRiskSummaryModel.$dirty"> Please supply a description.</span>
                <span class="error" v-if="!v$.rfcRiskSummaryModel.maxLength"> Sorry - too many characters.</span>
            </label><br>
            <editor
               :init="{
                 height: 500,
                 menubar: false,
                 plugins: 'lists',
                  toolbar: [
                     'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                     'bold italic strikethrough underline backcolor | ' +
                     'bullist numlist outdent indent | removeformat'
                  ]}"
               v-bind:content_css="false"
               v-bind:skin="false"
               v-bind:disabled="isReadOnly"
               v-model="rfcRiskSummaryModel"
            />
        </div>
    </div>
</template>

<script>
    import useVuelidate from '@vuelidate/core'
    import { required, maxLength } from '@vuelidate/validators'

    export default {
        name: "RfcRisk",
        setup() {
            return { v$: useVuelidate(), }
        },
        props: {
            isReadOnly: {
                type: Boolean,
                default: false,
            },
            rfcResults: {
                type: Array,
                default: function() {
                    return [];
                },
            },
        },
        data: () => ({
            rfcPriority: [
                { label: 'Critical', value: 4 },
                { label: 'High', value: 3 },
                { label: 'Medium', value: 2 },
                { label: 'Low', value: 1 },
            ],
            rfcPriorityModel: '',
            rfcRisk: [
                { label: 'Very High', value: 5 },
                { label: 'High', value: 4 },
                { label: 'Moderate', value: 3 },
                { label: 'Low', value: 2 },
                { label: 'None', value: 1 },
            ],
            rfcRiskModel: '',
            rfcRiskSummaryModel: '',
            rfcImpact: [
                { label: 'High', value: 3 },
                { label: 'Medium', value: 2 },
                { label: 'Low', value: 1 },
            ],
            rfcImpactModel: '',
        }),
        validations: {
            rfcPriorityModel: {
                required,
            },
            rfcRiskModel: {
                required,
            },
            rfcRiskSummaryModel: {
                required,
                maxLength: maxLength(630000),
            },
            rfcImpactModel: {
                required,
            },
        },
        methods: {
            updateValidation: function() {
                this.v$.$touch();

                this.$emit('update_validation', {
                    'tab': 'tab_2',
                    'value': !this.v$.$invalid,
                });
            },
            updateValues: function(modelName,modelValue) {
                this.$emit('update_values',{
                    'modelName': modelName,
                    'modelValue': modelValue,
                });
            },
        },
        watch: {
            rfcPriority: function() {
                this.updateValues('rfcPriority',this.rfcPriority);
                this.updateValidation();
            },
            rfcPriorityModel: function() {
                this.updateValues('rfcPriorityModel',this.rfcPriorityModel)
                this.updateValidation();
            },
            rfcRisk: function() {
                this.updateValues('rfcRisk',this.rfcRisk)
                this.updateValidation();
            },
            rfcRiskModel: function() {
                this.updateValues('rfcRiskModel',this.rfcRiskModel)
                this.updateValidation();
            },
            rfcRiskSummaryModel: function() {
                this.updateValues('rfcRiskSummaryModel',this.rfcRiskSummaryModel)
                this.updateValidation();
            },
            rfcImpact: function() {
                this.updateValues('rfcImpact',this.rfcImpact)
                this.updateValidation();
            },
            rfcImpactModel: function() {
                this.updateValues('rfcImpactModel',this.rfcImpactModel)
                this.updateValidation();
            },
        },
        mounted() {
            //When template loads - check to see if there is any data within the rfcResults. If so -> update all models
            if (this.rfcResults.length > 0) {
                // Filter for the correct rfcPriority
                this.rfcPriorityModel = this.rfcPriority.filter(row => {
                    return row['value'] === this.rfcResults[0]['fields']['rfc_priority'];
                })[0];

                //Filter for the correct rfcRisk
                this.rfcRiskModel = this.rfcRisk.filter(row => {
                    return row['value'] === this.rfcResults[0]['fields']['rfc_risk'];
                })[0];

                this.rfcRiskSummaryModel = this.rfcResults[0]['fields']['rfc_risk_and_impact_analysis'];

                //Filter for the correct rfc Impact
                this.rfcImpactModel = this.rfcImpact.filter(row => {
                    return row['value'] === this.rfcResults[0]['fields']['rfc_impact'];
                })[0];
            }

            //Just run the validations to show the error messages
            this.v$.$touch();
        }
    }
</script>

<style scoped>

</style>

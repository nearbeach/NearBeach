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
                    <label>Priority of Change</label>
                    <v-select v-bind:options="rfcPriority"
                              v-bind:disabled="isReadOnly"
                              v-model="rfcPriorityModel"
                    ></v-select>
                </div>
                <div class="col-md-4">
                    <label>Risk of Change</label>
                    <v-select v-bind:options="rfcRisk"
                              v-bind:disabled="isReadOnly"
                              v-model="rfcRiskModel"
                    ></v-select>
                </div>
                <div class="col-md-4">
                    <label>Impact of Change</label>
                    <v-select v-bind:options="rfcImpact"
                              v-bind:disabled="isReadOnly"
                              v-model="rfcImpactModel"
                    ></v-select>
                </div>
            </div>
            <br/>

            <!-- RFC SUMMARY -->
            <label>Risk Association:
<!--                <span class="error" v-if="!$v.projectDescriptionModel.required && $v.projectDescriptionModel.$dirty"> Please supply a description.</span>-->
<!--                <span class="error" v-if="!$v.projectDescriptionModel.maxLength"> Sorry - too many characters.</span>-->
            </label><br>
            <img src="/static/NearBeach/images/placeholder/body_text.svg"
                 class="loader-image"
                 alt="loading image for Tinymce"
            />
            <editor
               :init="{
                 height: 500,
                 menubar: false,
                 toolbar: 'undo redo | formatselect | ' +
                  'bold italic backcolor | alignleft aligncenter ' +
                  'alignright alignjustify | bullist numlist outdent indent | ',
               }"
               v-bind:content_css="false"
               v-bind:skin="false"
               v-bind:disabled="isReadOnly"
               v-model="rfcRiskSummaryModel"
            />
        </div>
    </div>
</template>

<script>
    export default {
        name: "RfcRisk",
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
        methods: {
            updateValues: function(modelName,modelValue) {
                this.$emit('update_values',{
                    'modelName': modelName,
                    'modelValue': modelValue,
                });
            },
        },
        watch: {
            rfcPriority: function() {
                this.updateValues('rfcPriority',this.rfcPriority)
            },
            rfcPriorityModel: function() {
                this.updateValues('rfcPriorityModel',this.rfcPriorityModel)
            },
            rfcRisk: function() {
                this.updateValues('rfcRisk',this.rfcRisk)
            },
            rfcRiskModel: function() {
                this.updateValues('rfcRiskModel',this.rfcRiskModel)
            },
            rfcRiskSummaryModel: function() {
                this.updateValues('rfcRiskSummaryModel',this.rfcRiskSummaryModel)
            },
            rfcImpact: function() {
                this.updateValues('rfcImpact',this.rfcImpact)
            },
            rfcImpactModel: function() {
                this.updateValues('rfcImpactModel',this.rfcImpactModel)
            },
        },
        mounted() {
            //When template loads - check to see if there is any data within the rfcResults. If so -> update all models
            if (this.rfcResults.length > 0) {
                // Filter for the correct rfcPriority
                this.rfcPriorityModel = this.rfcPriority.filter(row => {
                    return row['value'] === this.rfcResults[0]['fields']['rfc_priority'];
                });

                //Filter for the correct rfcRisk
                this.rfcRiskModel = this.rfcRisk.filter(row => {
                    return row['value'] === this.rfcResults[0]['fields']['rfc_risk'];
                });

                this.rfcRiskSummaryModel = this.rfcResults[0]['fields']['rfc_risk_and_impact_analysis'];

                //Filter for the correct rfc Impact
                this.rfcImpactModel = this.rfcImpact.filter(row => {
                    return row['value'] === this.rfcResults[0]['fields']['rfc_impact'];
                });
            }
        }
    }
</script>

<style scoped>

</style>
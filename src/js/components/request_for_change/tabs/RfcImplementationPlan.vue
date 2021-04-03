<template>
    <div class="row">
        <div class="col-md-4">
            <h2>Implementation Plan</h2>
            <p class="text-instructions">
                Please outline your implementation plan for this request for change.
            </p>
        </div>
        <div class="col-md-8" style="min-height: 610px;">
            <label>Implementation Plan:
                <span class="error" v-if="!$v.rfcImplementationPlanModel.required && $v.rfcImplementationPlanModel.$dirty"> Please supply a description.</span>
                <span class="error" v-if="!$v.rfcImplementationPlanModel.maxLength"> Sorry - too many characters.</span>
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
               v-model="rfcImplementationPlanModel"
            />
        </div>
    </div>
</template>

<script>
    import { required, maxLength } from 'vuelidate/lib/validators';

    export default {
        name: "RfcImplementationPlan",
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
            }
        },
        data: () => ({
            rfcImplementationPlanModel: '',
        }),
        validations: {
            rfcImplementationPlanModel: {
                required,
                maxLength: maxLength(630000),
            },
        },
        methods: {
            updateValidation: function() {
                this.$v.$touch();

                this.$emit('update_validation', {
                    'tab': 'tab_3',
                    'value': !this.$v.$invalid,
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
            rfcImplementationPlanModel: function() {
                this.updateValues('rfcImplementationPlanModel',this.rfcImplementationPlanModel);
                this.updateValidation();
            }
        },
        mounted() {
            //If the rfcResults are imported, update the rfcImplementationPlan
            if (this.rfcResults.length > 0) {
                this.rfcImplementationPlanModel = this.rfcResults[0]['fields']['rfc_implementation_plan'];
            }
        }
    }
</script>

<style scoped>

</style>
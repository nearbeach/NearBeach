<template>
    <div class="row">
        <div class="col-md-4">
            <h2>Test Plan</h2>
            <p class="text-instructions">
                Outline your test plan. How will you test the Request for Change once it has been implemented.
            </p>
        </div>
        <div class="col-md-8" style="min-height: 610px;">
            <label>Test Plan:
                <span class="error" v-if="!v$.rfcTestPlanModel.required && v$.rfcTestPlanModel.$dirty"> Please supply a description.</span>
                <span class="error" v-if="!v$.rfcTestPlanModel.maxLength"> Sorry - too many characters.</span>
            </label><br>
            <editor
               :init="{
                 height: 500,
                 menubar: false,
                 plugins: ['lists','table'],
                  toolbar: [
                     'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                     'bold italic strikethrough underline backcolor | table | ' +
                     'bullist numlist outdent indent | removeformat'
                  ]}"
               v-bind:content_css="false"
               v-bind:skin="false"
               v-bind:disabled="isReadOnly"
               v-model="rfcTestPlanModel"
            />
        </div>
    </div>
</template>

<script>
    import useVuelidate from '@vuelidate/core'
    import { required, maxLength } from '@vuelidate/validators'
    import Editor from '@tinymce/tinymce-vue';

    export default {
        name: "RfcTestPlan",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            'editor': Editor,
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
            rfcTestPlanModel: '',
        }),
        validations: {
            rfcTestPlanModel: {
                required,
                maxLength: maxLength(630000),
            }
        },
        methods: {
            updateValidation: function() {
                this.v$.$touch();

                this.$emit('update_validation', {
                    'tab': 'tab_5',
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
            rfcTestPlanModel: function() {
                this.updateValues('rfcTestPlanModel',this.rfcTestPlanModel);
                this.updateValidation();
            },
        },
        mounted() {
            //If the rfc results import - update the rfcBackout Model
            if (this.rfcResults.length > 0) {
                this.rfcTestPlanModel = this.rfcResults[0]['fields']['rfc_test_plan'];
            }
        }
    }
</script>

<style scoped>

</style>

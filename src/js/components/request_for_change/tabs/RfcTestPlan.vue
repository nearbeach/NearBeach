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
               v-model="rfcTestPlanModel"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: "RfcTestPlan",
    props: {
        rfcResults: {
            type: Array,
            default: function() {
                return [];
            },
        }
    },
    data: () => ({
        rfcTestPlanModel: '',
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
        rfcTestPlanModel: function() {
            this.updateValues('rfcTestPlanModel',this.rfcTestPlanModel);
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
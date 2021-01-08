<template>
    <div class="row">
        <div class="col-md-4">
            <h2>Description</h2>
            <p class="text-instructions">
                Place a detailed description here. This should cover what your Request For Change (RFC) will entail and
                why it should be implemented within the time frames specified below.
            </p>
        </div>
        <div class="col-md-8" style="min-height: 610px;">
            <div class="form-group">
                <label>Request for Change Title: </label>
                <input type="text"
                       maxlength="255"
                       class="form-control"
                       v-model="rfcTitleModel"
                />
            </div>
            <br/>

            <!-- RFC SUMMARY -->
            <label>Request for Change Summary:
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
               v-model="rfcSummaryModel"
            />
        </div>
    </div>
</template>

<script>
    export default {
        name: "RfcDescription",
        props: {
            rfcResults: {
                type: Array,
                default: function() {
                    return [];
                }
            }
        },
        data: () => ({
            rfcSummaryModel: '',
            rfcTitleModel: '',

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
            rfcSummaryModel: function() {
                this.updateValues('rfcSummaryModel',this.rfcSummaryModel);
            },
            rfcTitleModel: function() {
                this.updateValues('rfcTitleModel',this.rfcTitleModel);
            },
        },
        mounted() {
            //If there is data in the rfcResults - we will update the rfcSummary and rfcTitle
            if (this.rfcResults.length > 0) {
                this.rfcSummaryModel = this.rfcResults[0]['fields']['rfc_summary'];
                this.rfcTitleModel = this.rfcResults[0]['fields']['rfc_title'];
            }
        }
    }
</script>

<style scoped>

</style>
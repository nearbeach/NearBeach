<template>
    <div class="row">
        <div class="col-md-4">
            <h2>Backout Plan</h2>
            <p class="text-instructions">
                Please outline the backout plan that will be implemented, and when it will be implemented, when something
                goes wrong with the Request for Change.
            </p>
        </div>
        <div class="col-md-8" style="min-height: 610px;">
            <label>Backout Plan:
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
               v-model="rfcBackoutPlan"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: "RfcBackoutPlan",
    props: {},
    data: () => ({
        rfcBackoutPlan: '',
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
        rfcBackoutPlan: function() {
            this.updateValues('rfcBackoutPlan',this.rfcBackoutPlan)
        },
    },
}
</script>

<style scoped>

</style>
<template>
    <div class="row">
        <div class="col-md-4">
            <h2>Test Plan</h2>
            <p class="text-instructions">
                ...
            </p>
        </div>
        <div class="col-md-8" style="min-height: 610px;">
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
               v-model="rfcTestPlan"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: "RfcTestPlan",
    props: {},
    data: () => ({
        rfcTestPlan: '',
    })
}
</script>

<style scoped>

</style>
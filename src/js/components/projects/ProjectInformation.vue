<template>
    <div class="card">
        <div class="card-body">
            <h1>Project Information</h1>
            <hr>

            <div class="row">
                <!-- DESCRIPTION -->
                <div class="col-md-4">
                    <h2>Description</h2>
                    <p class="text-instructions">
                        Edit the project information and then click the "Update Project" button at the bottom of the
                        page
                    </p>
                </div>

                <!-- PROJECT FORM -->
                <div class="col-md-8" style="min-height: 610px;">
                    <!-- PROJECT NAME -->
                    <div class="form-group">
                        <label>Project Name
                            <span class="error" v-if="!$v.projectNameModel.required && $v.projectNameModel.$dirty"
                            > Please suppy a title.</span>
                        </label>
                        <input type="text"
                               v-model="projectNameModel"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- PROJECT DESCRIPTION -->
                    <label>Project Description:
                        <span class="error" v-if="!$v.projectDescriptionModel.required && $v.projectDescriptionModel.$dirty"> Please supply a description.</span>
                        <span class="error" v-if="!$v.projectDescriptionModel.maxLength"> Sorry - too many characters.</span>
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
                       v-model="projectDescriptionModel"
                    />
                </div>


            </div>

            <!-- STAKEHOLDER ORGANISATION -->
            <hr>
            <stakeholder-information v-bind:organisation-results="organisationResults"
                                     v-bind:default-stakeholder-image="defaultStakeholderImage"
            ></stakeholder-information>

            <!-- START DATE & END DATE -->
            <hr>
            <between-dates destination="project"
                           v-on:update_dates="updateDates($event)"
                           v-bind:is-dirty-end="$v.projectEndDateModel.$dirty || $v.projectStartDateModel.$dirty"
            ></between-dates>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateProject"
                    >Update Project</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import { Modal } from "bootstrap";

    //Validations
    import { required, maxLength } from 'vuelidate/lib/validators';

    export default {
        name: "ProjectInformation",
        props: {
            defaultStakeholderImage: String,
            organisationResults: Array,
            projectResults: Array,
        },
        data() {
            return {
                projectDescriptionModel: this.projectResults[0]['fields']['project_description'],
                projectEndDateModel: this.projectResults[0]['fields']['project_end_date'],
                projectNameModel: this.projectResults[0]['fields']['project_name'],
                projectStartDateModel: this.projectResults[0]['fields']['project_start_date'],
            }
        },
        validations: {
            projectDescriptionModel: {
              required,
              maxLength: maxLength(630000),
            },
            projectEndDateModel: {
                required,
            },
            projectNameModel: {
                required,
            },
            projectStartDateModel: {
                required,
            },
        },
        methods: {
            updateDates: function(data) {
                this.projectEndDateModel = data['end_date'];
                this.projectStartDateModel = data['start_date'];
            },
            updateProject: function() {
                // Check the validation first
                this.$v.$touch();

                if (this.$v.$invalid) {
                    //Show the error dialog and notify to the user that there were field missing.
                    var elem_cont = document.getElementById("errorModalContent");

                    // Update the content
                    elem_cont.innerHTML =
                        `<strong>FORM ISSUE:</strong> Sorry, but can you please fill out the form completely.`;

                    // Show the modal
                    var errorModal = new Modal(document.getElementById('errorModal'));
                    errorModal.show();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                //Construct data_to_send to backend
                const data_to_send = new FormData();
                data_to_send.set('project_description',this.projectDescriptionModel);
                data_to_send.set('project_end_date',this.projectEndDateModel);
                data_to_send.set('project_name',this.projectNameModel);
                data_to_send.set('project_start_date',this.projectStartDateModel);

                //Open up the loading modal
                var loadingModal = new Modal(document.getElementById('loadingModal'));
                loadingModal.show();

                //Update message in loading modal
                document.getElementById("loadingModalContent").innerHTML = `Updating your Requirement details`;

                //Use axios to send data
                axios.post(
                    `/project_information/${this.projectResults[0]['pk']}/save/`,
                    data_to_send
                ).then(response => {
                    //Update the message in the loading modal
                    document.getElementById("loadingModalContent").innerHTML = `UPDATED SUCCESSFULLY`;

                    //Close after 1 second
                    setTimeout(() => {
                        loadingModal.hide();
                    },1000);
                }).catch(error => {
                    console.log("Error: ",error);
                })

            },
        },
    }
</script>

<style scoped>

</style>
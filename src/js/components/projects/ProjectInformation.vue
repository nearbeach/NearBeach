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
                            > Please supply a title.</span>
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
                       v-bind:content_css="false"
                       v-bind:skin="false"
                       v-bind:disabled="isReadOnly"
                       v-model="projectDescriptionModel"
                    />
                </div>
            </div>

            <!-- PROJECT STATUS -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>Project Status</strong>
                    <p class="text-instructions">
                        Please update the project's task to reflect it's current status. Then click on the "Update
                        Project" button to save the change.
                    </p>
                </div>
                <div class="col-md-4"
                     v-if="!isReadOnly"
                >
                    <v-select v-bind:options="statusOptions"
                              v-model="projectStatusModel"
                    ></v-select>
                </div>
                <div class="col-md-4"
                     v-if="!isReadOnly"
                >
                    <div class="alert alert-danger"
                         v-if="projectStatusModel === 'Closed'"
                    >
                        Saving the project with this status will close the project.
                    </div>
                </div>
                <div class="col-md-4"
                     v-if="isReadOnly"
                >
                    <div class="alert alert-info"
                         v-if="projectStatusModel === 'Closed'"
                    >
                        Project has been closed.
                    </div>
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
                           v-bind:end-date-model="projectEndDateModel"
                           v-bind:start-date-model="projectStartDateModel"
            ></between-dates>

            <!-- Submit and Close Button -->
            <hr v-if="userLevel >= 2 && !isReadOnly">
            <div class="row submit-row"
                 v-if="!isReadOnly"
            >
                <div class="col-md-12">
                    <!-- Close Project -->
                    <a href="javascript:void(0)"
                       v-if="userLevel >= 3"
                       class="btn btn-danger"
                       v-on:click="closeProject"
                    >Close Project</a>

                    <!-- Update Project -->
                    <a href="javascript:void(0)"
                       v-if="userLevel >= 2"
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
    import { DateTime } from "luxon";

    //Validations
    import { required, maxLength } from 'vuelidate/lib/validators';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    export default {
        name: "ProjectInformation",
        props: {
            defaultStakeholderImage: String,
            organisationResults: Array,
            projectResults: Array,
            userLevel: {
              type: Number,
              default: 1,
            },
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
        data() {
            return {
                isReadOnly: false,
                projectDescriptionModel: this.projectResults[0]['fields']['project_description'],
                projectEndDateModel: DateTime.fromISO(this.projectResults[0]['fields']['project_end_date']),
                projectNameModel: this.projectResults[0]['fields']['project_name'],
                projectStartDateModel: DateTime.fromISO(this.projectResults[0]['fields']['project_start_date']),
                projectStatusModel: this.projectResults[0]['fields']['project_status'],
                statusOptions: [
                    'Backlog',
                    'Blocked',
                    'In Progress',
                    'Test/Review',
                ],
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
            closeProject: function() {
                //Set the project status to Closed
                this.projectStatusModel = 'Closed';

                //Update the project
                this.updateProject();
            },
            updateDates: function(data) {
                this.projectEndDateModel = data['end_date'];
                this.projectStartDateModel = data['start_date'];
            },
            updateProject: function() {
                // Check the validation first
                this.$v.$touch();

                if (this.$v.$invalid) {
                    this.showValidationErrorModal();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                //Construct data_to_send to backend
                const data_to_send = new FormData();
                data_to_send.set('project_description',this.projectDescriptionModel);
                data_to_send.set('project_end_date',this.projectEndDateModel);
                data_to_send.set('project_name',this.projectNameModel);
                data_to_send.set('project_start_date',this.projectStartDateModel);
                data_to_send.set('project_status', this.projectStatusModel);

                //Open up the loading modal
                this.showLoadingModal('Project');

                //Use axios to send data
                axios.post(
                    `/project_information/${this.projectResults[0]['pk']}/save/`,
                    data_to_send
                ).then(response => {
                    //Notify user of success update
                    this.closeLoadingModal();

                    //Reload the page IF the status is closed
                    window.location.reload(this.projectStatusModel === 'Closed');
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })
            },
        },
        mounted() {
            //If users have enough permissions add in the "Closed" functionaly
            if (this.userLevel >= 3) {
                this.statusOptions.push('Closed')
            }

            //If the project status is closed => set the isReadOnly to true
            this.isReadOnly = this.projectResults[0]['fields']['project_status'] === 'Closed';
        }
    }
</script>

<style scoped>

</style>

<template>
    <div class="card">
        <div class="card-body">
            <h1>New Task</h1>
            <hr>

            <div class="row">
                <!-- DESCRIPTION -->
                <div class="col-md-4">
                    <h2>Description</h2>
                    <p class="text-instructions">
                        To create a new task, fill out the form and submit at the bottom of the page.
                    </p>
                </div>

                <!-- Task FORM -->
                <div class="col-md-8" style="min-height: 610px;">
                    <!-- TASK NAME -->
                    <div class="form-group">
                        <label>Task Short Description:
                            <span class="error" v-if="!$v.taskShortDescriptionModel.required && $v.taskShortDescriptionModel.$dirty"
                            > Please supply a title.</span>
                        </label>
                        <input type="text"
                               v-model="taskShortDescriptionModel"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- TASK DESCRIPTION -->
                    <label>Task Long Description:
                        <span class="error" v-if="!$v.taskDescriptionModel.required && $v.taskDescriptionModel.$dirty"> Please supply a description.</span>
                        <span class="error" v-if="!$v.taskDescriptionModel.maxLength"> Sorry - too many characters.</span>
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
                       v-model="taskDescriptionModel"
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
            <between-dates destination="task"
                           v-on:update_dates="updateDates($event)"
                           v-bind:is-dirty-end="$v.taskEndDateModel.$dirty || $v.taskStartDateModel.$dirty"
                           v-bind:start-date-model="taskStartDateModel"
                           v-bind:end-date-model="taskEndDateModel"
            ></between-dates>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateTask"
                    >Update Task</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import { required, maxLength } from 'vuelidate/lib/validators';
    import { DateTime } from "luxon";

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    export default {
        name: "TaskInformation",
        props: {
            groupResults: Array,
            stakeholderModel: Array,
            taskResults: Array,
            organisationResults: Array,
            defaultStakeholderImage: String,
        },
        data() {
            return {
                taskDescriptionModel: this.taskResults[0]['fields']['task_long_description'],
                taskEndDateModel: DateTime.fromISO(this.taskResults[0]['fields']['task_end_date']),
                taskShortDescriptionModel: this.taskResults[0]['fields']['task_short_description'],
                taskStartDateModel: DateTime.fromISO(this.taskResults[0]['fields']['task_start_date']),
            }
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
        validations: {
            taskDescriptionModel: {
                required,
                maxLength: maxLength(630000),
            },
            taskEndDateModel: {
                required,
            },
            taskShortDescriptionModel: {
                required,
            },
            taskStartDateModel: {
                required,
            },
        },
        methods: {
            updateTask: function() {
                //Check validation
                this.$v.$touch();

                //If the form is not validated
                if (this.$v.$invalid) {
                    this.showValidationErrorModal();

                    //User does not need to do anything else
                    return;
                }

                //Show the saving modal
                this.showLoadingModal('task');

                //Create the data_to_send array
                const data_to_send = new FormData();
                data_to_send.set('task_long_description',this.taskDescriptionModel);
                data_to_send.set('task_end_date',this.taskEndDateModel);
                data_to_send.set('task_short_description',this.taskShortDescriptionModel);
                data_to_send.set('task_start_date',this.taskStartDateModel);

                //Send data to backend
                axios.post(
                    `/task_information/${this.taskResults[0]['pk']}/save/`,
                    data_to_send
                ).then(response => {
                    //Hide the loading modal
                    this.closeLoadingModal();
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                });
            },
            updateDates: function(data) {
                this.taskEndDateModel = data['end_date'];
                this.taskStartDateModel = data['start_date'];
            },
            updateGroupModel: function(data) {
                this.groupModel = data;
            },
            updateStakeholderModel: function(data) {
                this.stakeholderModel = data;
            }
        }
    }
</script>

<style scoped>

</style>

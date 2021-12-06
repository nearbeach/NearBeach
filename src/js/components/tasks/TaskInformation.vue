<template>
    <div class="card">
        <div class="card-body">
            <h1>Task Information</h1>
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
                    <img v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
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

            <!-- TASK STATUS -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>Task Status</strong>
                    <p class="text-instructions">
                        Please update the task's status to reflect it's current status. Then click on the "Update
                        Task" button to save the change.
                    </p>
                </div>
                <div class="col-md-4"
                     v-if="!isReadOnly"
                >
                    <v-select v-bind:options="statusOptions"
                              v-model="taskStatusModel"
                    ></v-select>
                </div>
                <div class="col-md-4"
                     v-if="!isReadOnly"
                >
                    <div class="alert alert-danger"
                         v-if="taskStatusModel === 'Closed'"
                    >
                        Saving the task with this status will close the task.
                    </div>
                </div>
                <div class="col-md-4"
                     v-if="isReadOnly"
                >
                    <div class="alert alert-info"
                         v-if="taskStatusModel === 'Closed'"
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
            <between-dates destination="task"
                           v-on:update_dates="updateDates($event)"
                           v-bind:is-dirty-end="$v.taskEndDateModel.$dirty || $v.taskStartDateModel.$dirty"
                           v-bind:start-date-model="taskStartDateModel"
                           v-bind:end-date-model="taskEndDateModel"
            ></between-dates>

            <!-- Submit Button -->
            <hr v-if="userLevel >= 2 && !isReadOnly">
            <div class="row submit-row"
                 v-if="!isReadOnly"
            >
                <div class="col-md-12">
                    <!-- Close Task -->
                    <a href="javascript:void(0)"
                       v-if="userLevel >= 3"
                       class="btn btn-danger"
                       v-on:click="closeTask"
                    >Close Task</a>

                    <!-- Update Task -->
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-if="userLevel >= 2"
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

    //VueX
    import { mapGetters } from 'vuex';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    export default {
        name: "TaskInformation",
        props: {
            defaultStakeholderImage: String,
            groupResults: Array,
            stakeholderModel: Array,
            taskResults: Array,
            organisationResults: Array,
            userLevel: {
              type: Number,
              default: 1,
            },
        },
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            }),
        },
        data() {
            return {
                isReadOnly: false,
                statusOptions: [
                    'Backlog',
                    'Blocked',
                    'In Progress',
                    'Test/Review',
                ],
                taskDescriptionModel: this.taskResults[0]['fields']['task_long_description'],
                taskEndDateModel: DateTime.fromISO(this.taskResults[0]['fields']['task_end_date']),
                taskShortDescriptionModel: this.taskResults[0]['fields']['task_short_description'],
                taskStartDateModel: DateTime.fromISO(this.taskResults[0]['fields']['task_start_date']),
                taskStatusModel: this.taskResults[0]['fields']['task_status'],
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
            closeTask: function() {
                //Set the status to closed
                this.taskStatusModel = 'Closed';

                //Save the status
                this.updateTask();
            },
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
                data_to_send.set('task_status', this.taskStatusModel);

                //Send data to backend
                axios.post(
                    `${this.rootUrl}task_information/${this.taskResults[0]['pk']}/save/`,
                    data_to_send
                ).then(response => {
                    //Hide the loading modal
                    this.closeLoadingModal();

                    //Reload the page IF the status is closed
                    if (this.taskStatusModel === 'Closed') {
                        window.location.reload(this.taskStatusModel === 'Closed');
                    }
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
        },
        mounted() {
            //If users have enough permissions add in the "Closed" functionaly
            if (this.userLevel >= 3) {
                this.statusOptions.push('Closed')
            }

            //If the project is closed -> we state that is read only is true
            this.isReadOnly = this.taskResults[0]['fields']['task_status'] === 'Closed';
        },
    }
</script>

<style scoped>

</style>

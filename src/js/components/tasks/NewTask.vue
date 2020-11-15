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
            <get-stakeholders v-on:update_stakeholder_model="updateStakeholderModel($event)"
                              v-bind:is-dirty="$v.stakeholderModel.$dirty"
            ></get-stakeholders>

            <!-- START DATE & END DATE -->
            <hr>
            <between-dates destination="task"
                           v-on:update_dates="updateDates($event)"
                           v-bind:is-dirty-end="$v.taskEndDateModel.$dirty || $v.taskStartDateModel.$dirty"
            ></between-dates>

            <!-- Group Permissions -->
            <hr>
            <group-permissions v-bind:group-results="groupResults"
                               v-bind:destination="'task'"
                               v-on:update_group_model="updateGroupModel($event)"
                               v-bind:is-dirty="$v.groupModel.$dirty"
            ></group-permissions>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="submitNewTask"
                    >Create new Task</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import { required, maxLength } from 'vuelidate/lib/validators';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    export default {
        name: "NewTask",
        props: {
            groupResults: Array,
        },
        data() {
            return {
                groupModel: {},
                stakeholderModel: '',
                taskDescriptionModel: '',
                taskEndDateModel: '',
                taskShortDescriptionModel: '',
                taskStartDateModel: '',
            }
        },
        mixins: [
            errorModalMixin,
        ],
        validations: {
            groupModel: {
                required,
            },
            stakeholderModel: {
                required,
            },
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
            submitNewTask: function() {
                //Check validation
                this.$v.$touch();

                //If the form is not validated
                if (this.$v.$invalid) {
                    this.showValidationErrorModal();

                    //User does not need to do anything else
                    return;
                }

                //Create the data_to_send array
                const data_to_send = new FormData();
                data_to_send.set('organisation',this.stakeholderModel['value']);
                data_to_send.set('task_long_description',this.taskDescriptionModel);
                data_to_send.set('task_end_date',this.taskEndDateModel);
                data_to_send.set('task_short_description',this.taskShortDescriptionModel);
                data_to_send.set('task_start_date',this.taskStartDateModel);

                // Insert a new row for each group list item
                this.groupModel.forEach((row,index) => {
                    data_to_send.append(`group_list`,row['value']);
                });

                //Send data to backend
                axios.post(
                    '/new_task/save/',
                    data_to_send
                ).then(response => {
                    //Go to the new project
                    window.location.href = response['data'];
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

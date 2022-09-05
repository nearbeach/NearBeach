<template>
    <div class="card">
        <div class="card-body">
            <h1>Change Task - {{changeTaskResults[0]['pk']}}</h1>
            <hr>

            <!-- CHANGE TASK TITLE -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Change Task Title</strong>
                    <p class="text-instructions">
                        Please write a short title of the description for this task. i.e Backup of Database
                    </p>
                </div>
                <div class="col-md-8">
                    <div class="form-group">
                        <label>Change Title:</label>
                        <input type="text"
                               class="form-control"
                               v-model="changeTitleModel"/>
                    </div>
                </div>
            </div>

            <!-- START DATE & END DATE -->
            <hr>
            <between-dates destination="Change Task"
                           v-bind:start-date-model="changeStartDateModel"
                           v-bind:end-date-model="changeEndDateModel"
                           v-on:update_dates="updateDates($event)"
            ></between-dates>

            <!-- IMPLEMENTATION USER & QA USER -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>Implementation & QA User</strong>
                    <p class="text-instructions">
                        Please indicate which user will be implementing the work, and the user who will QA.
                    </p>
                </div>
                <div class="col-md-8">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <lable>Implementation User</lable>
                                <n-select v-bind:options="userListFixed"
                                            v-model:value="assignedUserModel"
                                ></n-select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <lable>QA User</lable>
                                <n-select v-model:value="qaUserModel" 
                                            v-bind:options="userListFixed" 
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- DESCRIPTION OPTIONAL -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>Description</strong>
                    <p class="text-instructions">
                        Write a detail description of this particular task.
                    </p>
                </div>
                <div class="col-md-8">
                    <label>Change Task Description (Optional):</label>
                    <editor
                       :init="{
                         height: 300,
                         menubar: false,
                         plugins: ['lists','table'],
                        toolbar: [
                           'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                           'bold italic strikethrough underline backcolor | table | ' +
                           'bullist numlist outdent indent | removeformat'
                        ]}"
                       v-bind:content_css="false"
                       v-bind:skin="false"
                       v-model="changeDescriptionModel"
                    />
                </div>
            </div>

            <!-- MISC -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>Misc</strong>
                    <p class="text-instructions">
                        Please fill in the stakeholders for this particular change task. Default value will be
                        "Stakeholders".
                    </p>
                    <p class="text-instructions">
                        To state if there is downtime, please click the "No Downtime" to change it's statue.
                    </p>
                </div>
                <div class="col-md-8">
                    <div class="form-group">
                        <label>Stakeholders:</label>
                        <input type="text"
                               class="form-control"
                               v-model="changeStakeholderModel"
                        />
                    </div>

                    <br/>
                    <div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">
                        <input type="checkbox"
                               id="isDowntime"
                               class="btn-check"
                               autocomplete="off"
                               v-model="changeIsDowntimeModel"
                        >
                        <label class="btn btn-outline-primary" for="isDowntime">{{isDowntime()}}</label>
                    </div>
                </div>
            </div>
            
            <!-- GO BACK -->
            <hr>
            <!-- CANCEL -->
            <a v-bind:href="`${rootUrl}rfc_information/${changeTaskResults[0]['fields']['request_for_change']}/`"
               class="btn btn-secondary cancel-changes"
            >Cancel</a>

            <!-- DELETE -->
            <a href="javascript:void(0)"
               class="btn btn-warning"
               v-if="changeTaskResults[0]['fields']['change_task_status'] == 1 && userLevel == 4"
               v-on:click="deleteChangeTask"
            >Delete</a>

            <!-- SAVE -->
            <a href="javascript:void(0)"
               class="btn btn-primary save-changes"
               v-if="changeTaskResults[0]['fields']['change_task_status'] == 1 && userLevel >= 2"
               v-on:click="saveChangeTask"
            >Save</a>

            <!-- START CHANGE TASK -->
            <a href="javascript:void(0)"
               class="btn btn-danger save-changes"
               v-if="changeTaskResults[0]['fields']['change_task_status'] == 3 && userLevel >= 2"
               v-on:click="updateStatus(4)"
            >Start Task</a>

            <!-- FINISH CHANGE TASK -->
            <a href="javascript:void(0)"
               class="btn btn-success save-changes"
               v-if="changeTaskResults[0]['fields']['change_task_status'] == 4 && userLevel >= 2"
               v-on:click="updateStatus(5)"
            >Finish Task</a>

            <!-- REJECT CHANGE TASK -->
            <a href="javascript:void(0)"
               class="btn btn-danger save-changes"
               v-if="changeTaskResults[0]['fields']['change_task_status'] == 4 && userLevel >= 2"
               v-on:click="updateStatus(6)"
            >REJECT Task</a>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import Editor from '@tinymce/tinymce-vue';
    import BetweenDates from "../dates/BetweenDates.vue";
    import { NSelect } from 'naive-ui';

    export default {
        name: "ChangeTaskInformation",
        components: {
            BetweenDates,
            'editor': Editor,
            NSelect,
        },
        props: {
            changeTaskResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            rootUrl: {
                type: String,
                default: '/',
            },
            userLevel: {
                type: Number,
                default: 0,
            },
            userList: {
                type: Array,
                default: () => {
                    return [];
                }
            },
        },
        data() {
            return {
                assignedUserModel: this.changeTaskResults[0]['fields']['change_task_assigned_user'],
                changeTitleModel: this.changeTaskResults[0]['fields']['change_task_title'],
                changeDescriptionModel: this.changeTaskResults[0]['fields']['change_task_description'],
                changeStakeholderModel: this.changeTaskResults[0]['fields']['change_task_required_by'],
                changeIsDowntimeModel: this.changeTaskResults[0]['fields']['is_downtime'],
                changeStartDateModel: new Date(this.changeTaskResults[0]['fields']['change_task_start_date']).getTime(),
                changeEndDateModel: new Date(this.changeTaskResults[0]['fields']['change_task_end_date']).getTime(),
                qaUserModel: this.changeTaskResults[0]['fields']['change_task_qa_user'],
                userListFixed: this.userList.map((row) => {
                    return {
                        label: `${row.username}: ${row.first_name} ${row.last_name}`,
                        value: row.id,
                    };
                })
            }
        },
        methods: {
            isDowntime: function() {
                if (this.changeIsDowntimeModel) {
                    return `Downtime Scheduled`;
                }
                return `No Downtime`;
            },
            deleteChangeTask: function() {
                //Send the trigger
                axios.post(
                    `${this.rootUrl}change_task_information/${this.changeTaskResults[0]['pk']}/delete/`,
                ).then(response => {
                    //If successful, go back
                    window.location.href = `${this.rootUrl}rfc_information/${this.changeTaskResults[0]['fields']['request_for_change']}/`;
                })
            },
            saveChangeTask: function(event) {
                //Stop the usual stuff
                event.preventDefault();

                var change_task_seconds = this.changeEndDateModel - this.changeStartDateModel

                // Create data_to_send
                const data_to_send = new FormData();
                data_to_send.set('change_task_title', this.changeTitleModel);
                data_to_send.set('change_task_description', this.changeDescriptionModel);
                data_to_send.set('change_task_start_date', new Date(this.changeStartDateModel).toISOString());
                data_to_send.set('change_task_end_date', new Date(this.changeEndDateModel).toISOString());
                data_to_send.set('change_task_seconds', change_task_seconds.toString());
                data_to_send.set('change_task_assigned_user', this.assignedUserModel);
                data_to_send.set('change_task_qa_user', this.qaUserModel);
                data_to_send.set('change_task_required_by', this.changeStakeholderModel);
                data_to_send.set('is_downtime', this.changeIsDowntimeModel);

                axios.post(
                    `${this.rootUrl}change_task_information/${this.changeTaskResults[0]['pk']}/save/`,
                    data_to_send,
                ).then(response => {
                    //If successful, go back
                    window.location.href = `${this.rootUrl}rfc_information/${this.changeTaskResults[0]['fields']['request_for_change']}/`;
                }).catch(error => {
                    //this.showErrorModal(error, 'Change Task');
                    
                })
            },
            updateStatus: function(new_status) {
                //Setup data_to_send
                const data_to_send = new FormData();
                data_to_send.set('change_task_status', new_status);

                //Use axios to send the data
                axios.post(
                    `${rootUrl}change_task_update_status/${this.changeTaskResults[0]['pk']}/`,
                    data_to_send,
                ).then(response => {
                    //Reload the page
                    window.location.reload(true);
                }).catch(error => {
                    
                })
            },
            updateDates: function(data) {
                this.changeStartDateModel = data['start_date'];
                this.changeEndDateModel = data['end_date'];
            },
        }
    }
</script>

<style scoped>
.save-changes {
    margin-left: 10px;
}
</style>

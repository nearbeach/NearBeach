<template>
    <div class="row">
        <div class="col-md-4">
            <strong>Run Sheet List</strong>
            <p class="text-instructions">
                The run sheet will specify specific tasks for each user to implement. Each run item can be specified to;
                <ul>
                    <li>Block other run items</li>
                    <li>Block out downtime</li>
                </ul>
            </p>
        </div>
        <div class="col-md-8">
            <table class="table"
                   v-if="changeTaskList.length > 0"
            >
                <thead>
                    <tr>
                        <td style="width: 20%;">Timings</td>
                        <td style="width: 55%;">Title</td>
                        <td style="width: 25%;">Assigned Users</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="changeTask in changeTaskList">
                        <td>
                            <div>Start Time:</div>
                            <div class="small-text">{{getNiceDate(changeTask['fields']['change_task_start_date'])}}</div>
                            <div class="spacer"></div>
                            <div>End Time:</div>
                            <div class="small-text">{{getNiceDate(changeTask['fields']['change_task_end_date'])}}</div>
                        </td>
                        <td>
                            <a v-bind:href="`/change_task_information/${changeTask['pk']}/`">{{changeTask['fields']['change_task_title']}}</a>
                        </td>
                        <td>
                            <div>Assigned User:</div>
                            <div class="small-text">{{getUserName(changeTask['fields']['change_task_assigned_user'])}}</div>
                            <div class="spacer"></div>
                            <div>QA User:</div>
                            <div class="small-text">{{getUserName(changeTask['fields']['change_task_qa_user'])}}</div>
                            <div class="spacer"></div>
                            <div>Status:</div>
                            <div class="small-text"
                                 v-if="rfcStatus !== 4"
                            >
                                {{getStatus(changeTask['fields']['change_task_status'])}}
                            </div>
                            <div v-else>
                                <!-- START BUTTON -->
                                <a href="javascript:void(0)"
                                   class="btn btn-primary change-task-button"
                                   v-on:click="updateChangeTaskStatus(changeTask['pk'],4)"
                                   v-if="changeTask['fields']['change_task_status']==3 && userLevel > 1"
                                >Start Task</a>

                                <!-- FINISH BUTTON -->
                                <a href="javascript:void(0)"
                                   class="btn btn-warning change-task-button"
                                   v-on:click="updateChangeTaskStatus(changeTask['pk'],5)"
                                   v-if="changeTask['fields']['change_task_status']==4 && userLevel > 1"
                                >Finish Task</a>

                                <!-- SUCCESS BUTTON -->
                                <a href="javascript:void(0)"
                                   class="btn btn-success change-task-button"
                                   v-if="changeTask['fields']['change_task_status']==5 && userLevel > 1"
                                >Successful</a>

                                <!-- FAILED BUTTON -->
                                <a href="javascript:void(0)"
                                   class="btn btn-danger change-task-button"
                                   v-if="changeTask['fields']['change_task_status']==6 && userLevel > 1"
                                >Failed</a>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div class="alert alert-primary"
                 v-if="changeTaskList.length == 0"
            >
                Currently there are no Change Tasks associated with this Request for Change. Please add some by clicking
                on the button below.
            </div>
        </div>

        <!-- ADD NEW CHANGE TASK TO RUN SHEET -->
        <hr v-if="!isReadOnly">
        <div class="row submit-row"
             v-if="!isReadOnly"
        >
            <div class="col-md-12">
                <a href="javascript:void(0)"
                   class="btn btn-primary save-changes"
                   v-on:click="addNewChangeItem"
                   v-if="userLevel > 1"
                >New Change Item</a>
            </div>
        </div>

        <!-- If ALL Change Tasks have been completed - you can close the RFC -->
        <div class="row submit-row"
             v-if="isCompleted"
        >
            <div class="col-md-12">
                <a href="javascript:void(0)"
                   class="btn btn-warning save-changes"
                   v-on:click="closeRfc"
                   v-if="userLevel > 1"
                >Close Request for Change</a>
            </div>
        </div>

        <!-- Modal -->
        <rfc-new-run-item v-bind:location-id="locationId"
                          v-on:update_change_task_list="updateChangeTaskList($event)"
                          v-if="!isReadOnly"
        ></rfc-new-run-item>
    </div>
</template>

<script>
    const axios = require('axios');
    import { Modal } from "bootstrap";

    // Mixins
    import datetimeMixins from "../../../mixins/datetimeMixins";
    import errorModalMixin from "../../../mixins/errorModalMixin";

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: "RfcRunSheetList",
        props: {
            isReadOnly: {
                type: Boolean,
                default: false,
            },
            locationId: Number,
            rfcId: Number,
            rfcStatus: {
                type: Number,
                default: 0,
            },
            userList: Array,
        },
        mixins: [
            errorModalMixin,
            datetimeMixins,
        ],
        data: () => ({
            changeTaskList: [],
        }),
        computed: {
            ...mapGetters({
                userLevel: "getUserLevel",
                rootUrl: "getRootUrl",
            }),
            isCompleted: function() {
                var count_of_uncompleted_tasks = this.changeTaskList.filter(changeTask => {
                    const change_task_status = changeTask['fields']['change_task_status'];
                    return change_task_status !== 5 && change_task_status !== 6;
                }).length;

                //Return true when there are no uncompleted tasks (all finished)
                return count_of_uncompleted_tasks === 0 && (this.rfcStatus === 3 || this.rfcStatus === 4);
            }
        },
        methods: {
            addNewChangeItem: function() {
                var newChangeTaskModal = new Modal(document.getElementById('newRunItemModal'));
                newChangeTaskModal.show();
            },
            closeRfc: function() {
                //Construct the data to send
                const data_to_send = new FormData();
                data_to_send.set('rfc_status', 5);

                axios.post(
                    `${this.rootUrl}rfc_information/${this.rfcId}/update_status/`,
                    data_to_send,
                ).then(response => {
                    //Refresh Page
                    window.location.reload(true);
                }).catch(error => {
                    this.showErrorModal(error, 'request_for_change');
                });
            },
            getRunSheetList: function() {
                axios.post(
                    `${this.rootUrl}rfc_information/${this.locationId}/change_task_list/`,
                ).then(response => {
                    // Update the changeTaskList
                    this.changeTaskList = response['data'];
                }).catch(error => {
                    this.showErrorModal(error, 'request_for_change');
                });    
            },
            getStatus: function(status_id) {
                switch(status_id) {
                    case 1:
                        return 'Draft';
                        
                    case 2:
                        return 'Waiting for approval';
                        
                    case 3:
                        return 'Waiting to start';
                        
                    case 4:
                        return 'Task Started';
                        
                    case 5:
                        return 'Task Finished';
                        
                    case 6:
                        return 'Task FAILED';
                        
                    default:
                        return '---';
                }
                
            },
            getUserName: function(user_id) {
                //Filter for the user by using the user_id
                var single_user = this.userList.filter(row => {
                    return row['id'] == user_id;
                });
                
                //If there are no results - default to ---
                if (single_user.length == 0) {
                    return '---';
                }
                
                //User was filtered out - return their name
                return `${single_user[0]['username']}: ${single_user[0]['first_name']} ${single_user[0]['last_name']}`;
            },
            updateChangeTaskList: function(data) {
                //Update change task list
                this.changeTaskList = data;
            },
            updateChangeTaskStatus: function(change_task_id,change_task_status) {
                //Construct data to send
                const data_to_send = new FormData()
                data_to_send.set('change_task_status',change_task_status)

                axios.post(
                    `${this.rootUrl}change_task_update_status/${change_task_id}/`,
                    data_to_send,
                ).then(response => {
                    /*
                    We are using the map function to make a single variable change without having to write a loop function.
                    The change task has been update, so we are only changing that task when mapping the results back
                    to itself.
                     */
                    this.changeTaskList = this.changeTaskList.map(changeTask => {
                        //The change task that we have just updated :)
                        if (changeTask['pk'] == change_task_id) {
                            //Update the change Task Status
                            changeTask['fields']['change_task_status'] = change_task_status;

                            //Send back the change task status
                            return changeTask;
                        } else {
                            // Not the change task we updated :(
                            return changeTask;
                        }
                    });
                }).catch(error => {
                    this.showErrorModal(error, 'request_for_change');
                })
            },
        },
        mounted() {
            // Get the run sheet list
            this.getRunSheetList();
        }
    }
</script>

<style scoped>

</style>

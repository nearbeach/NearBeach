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
                            <a href="#">{{changeTask['fields']['change_task_title']}}</a>
                        </td>
                        <td>
                            <div>Assigned User:</div>
                            <div class="small-text">{{getUserName(changeTask['fields']['change_task_assigned_user'])}}</div>
                            <div class="spacer"></div>
                            <div>QA User:</div>
                            <div class="small-text">{{getUserName(changeTask['fields']['change_task_qa_user'])}}</div>
                            <div class="spacer"></div>
                            <div>Status:</div>
                            <div class="small-text">{{getStatus(changeTask['fields']['change_task_status'])}}</div>
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
                >New Change Item</a>
            </div>
        </div>

        <!-- Modal -->
        <rfc-new-run-item v-bind:location-id="locationId"
                          v-on:update_change_task_list="updateChangeTaskList($event)"
        ></rfc-new-run-item>
    </div>
</template>

<script>
    const axios = require('axios');
    import { Modal } from "bootstrap";

    // Mixins
    import datetimeMixins from "../../../mixins/datetimeMixins";
    import errorModalMixin from "../../../mixins/errorModalMixin";

    export default {
        name: "RfcRunSheetList",
        props: {
            isReadOnly: {
                type: Boolean,
                default: false,
            },
            locationId: Number,
            userList: Array,
        },
        mixins: [
            errorModalMixin,
            datetimeMixins,
        ],
        data: () => ({
            changeTaskList: [],
        }),
        methods: {
            addNewChangeItem: function() {
                var newChangeTaskModal = new Modal(document.getElementById('newRunItemModal'));
                newChangeTaskModal.show();
            },
            getRunSheetList: function() {
                axios.post(
                    `/rfc_information/${this.locationId}/change_task_list/`,
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
                        break;
                    case 2:
                        return 'Waiting for approval';
                        break;
                    case 3:
                        return 'Waiting to start';
                        break;
                    case 4:
                        return 'Task Started';
                        break;
                    case 5:
                        return 'Task Finished';
                        break;
                    default:
                        return '---';
                }
                return '---';
            },
            getUserName: function(user_id) {
                //Filter for the user by using the user_id
                var single_user = this.userList.filter(row => {
                    return row['pk'] == user_id;
                });
                
                //If there are no results - default to ---
                if (single_user.length == 0) {
                    return '---';
                }
                
                //User was filtered out - return their name
                return `${single_user[0]['fields']['username']}: ${single_user[0]['fields']['first_name']} ${single_user[0]['fields']['last_name']}`;
            },
            updateChangeTaskList: function(data) {
                //Update change task list
                this.changeTaskList = data;
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

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
                        <td style="width: 10%;">Start Time</td>
                        <td style="width: 10%;">End Time</td>
                        <td style="width: 40%;">Title</td>
                        <td style="width: 15%;">Assigned User</td>
                        <td style="width: 15%;">QA User</td>
                        <td style="width: 10%;">Status</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="changeTask in changeTaskList">
                        <td>{{changeTask['fields']['change_task_start_date']}}</td>
                        <td>{{changeTask['fields']['change_task_end_date']}}</td>
                        <td>
                            <a href="#">{{changeTask['fields']['change_task_description']}}</a>
                        </td>
                        <td>{{changeTask['fields']['change_task_assigned_user']}}</td>
                        <td>{{changeTask['fields']['change_task_qa_user']}}</td>
                        <td>{{changeTask['fields']['change_task_status']}}</td>
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
        <rfc-new-run-item></rfc-new-run-item>
    </div>
</template>

<script>
    const axios = require('axios');

    // Mixins
    import errorModalMixin from "../../../mixins/errorModalMixin";

    export default {
        name: "RfcRunSheetList",
        props: {
            isReadOnly: {
                type: Boolean,
                default: false,
            },
            locationId: Number,
        },
        data: () => ({
            changeTaskList: [],
        }),
        methods: {
            addNewChangeItem: function() {
                //ADD CODE
            },
            getRunSheetList: function() {
                //ADD CODE TO GET DATA
            }
        }
    }
</script>

<style scoped>

</style>
<template>
    <div>
        <h2><i data-feather="compass"></i> Associated Objects</h2>
        <hr v-if="projectResults.length + taskResults.length > 0">

        <!-- Project Results -->
        <div class="row"
             v-if="projectResults.length > 0"
        >
            <div class="col-md-4">
                <strong>Project</strong>
                <p class="text-instructions">
                    The following are current OPEN projects associated with the organisation.
                </p>
            </div>
            <div class="col-md-8">
                <table class="table">
                    <thead>
                        <tr>
                            <td>Project Information</td>
                            <td>Status</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="project in projectResults">
                            <td>
                                <a v-bind:href="`/project_information/${project['project_id']}/`">
                                    <p>{{project['project_name']}}</p>
                                    <div class="spacer"></div>
                                    <p class="small-text">
                                        Project {{project['project_id']}} -
                                        End Date:
                                        {{getFriendlyDate(project['project_end_date'])}}
                                    </p>
                                </a>
                            </td>
                            <td>{{project['project_status']}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <!-- THE FOLLOWING HR WILL NEED TO BE FIXED! -->
        <hr v-if="projectResults.length > 0">

        <!-- Requirement Results -->
        <div class="row"
             v-if="requirementResults.length > 0"
        >
            <div class="col-md-4">
                <strong>Requirement</strong>
                <p class="text-instructions">
                    The following are current OPEN requirements associated with the organisation.
                </p>
            </div>
            <div class="col-md-8">
                <table class="table">
                    <thead>
                        <tr>
                            <td>Requirement Information</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="requirement in requirementResults">
                            <td>
                                <a v-bind:href="`/requirement_information/${requirement['requirement_id']}/`">
                                    <p>{{requirement['requirement_title']}}</p>
                                    <div class="spacer"></div>
                                    <p class="small-text">
                                        Requirement {{requirement['requirement_id']}}
                                    </p>
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <!-- THE FOLLOWING HR WILL NEED TO BE FIXED! -->
        <hr v-if="projectResults.length > 0">

        <!-- Task Results -->
        <div class="row"
             v-if="taskResults.length > 0"
        >
            <div class="col-md-4">
                <strong>Task</strong>
                <p class="text-instructions">
                    The following are current OPEN tasks associated with the organisation.
                </p>
            </div>
            <div class="col-md-8">
                <table class="table">
                    <thead>
                        <tr>
                            <td>Task Information</td>
                            <td>Status</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="task in taskResults">
                            <td>
                                <a v-bind:href="`/task_information/${task['task_id']}/`">
                                    <p>{{task['task_short_description']}}</p>
                                    <div class="spacer"></div>
                                    <p class="small-text">
                                        Task {{task['task_id']}} -
                                        End Date:
                                        {{getFriendlyDate(task['task_end_date'])}}
                                    </p>
                                </a>
                            </td>
                            <td>{{task['task_status']}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Only show when there are no associated tasks -->
        <div class="spacer"
             v-if="projectResults.length + taskResults.length === 0"
        ></div>

        <div class="alert alert-info"
             v-if="projectResults.length + taskResults.length === 0"
        >
            There are currently no Objects associated with this Organisation. You can create some new objects by
            click on the "New Objects" menu item.
        </div>

    </div>
</template>

<script>
    const axios = require('axios');

    export default {
        name: "AssociatedObjects",
        props: [
            'destination',
            'locationId',
        ],
        data() {
            return {
                opportunityResults: [],
                projectResults: [],
                requirementResults: [],
                taskResults: [],
            }
        },
        methods: {
            getAssociatedObjectResults: function() {
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/associated_objects/`,
                ).then(response => {
                    this.opportunityResults = response['data']['opportunity'];
                    this.projectResults = response['data']['project'];
                    this.requirementResults = response['data']['requirement'];
                    this.taskResults = response['data']['task'];
                }).catch(error => {
                    console.log("Error: ",error);
                })
            },
            getFriendlyDate: function(input_date) {
                var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
                    local_date = new Date(input_date);

                return local_date.toLocaleString("en-US",options);
            }
        },
        mounted() {
            this.getAssociatedObjectResults();
        }
    }
</script>

<style scoped>

</style>
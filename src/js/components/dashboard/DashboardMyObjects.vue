<template>
    <div class="card">
        <div class="card-body">
            <h1>My Current Objects</h1>
            <hr>

            <div class="alert alert-dark"
                 v-if="!isLoaded"
            >
                Still obtaining your assigned jobs.
            </div>
            
            <!-- Requirements -->
            <render-object-table v-if="objectResults.requirement.length > 0"
                                 v-bind:search-results="objectResults.requirement"
                                 v-bind:import-variables="requirementVariables"
                                 v-bind:destination="'requirement'"
                                 v-bind:root-url="rootUrl"
            ></render-object-table>

            <!-- Projects -->
            <render-object-table v-if="objectResults.project.length > 0"
                                 v-bind:search-results="objectResults.project"
                                 v-bind:import-variables="projectVariables"
                                 v-bind:destination="'project'"
                                 v-bind:root-url="rootUrl"
            ></render-object-table>

            <!-- Tasks -->
            <render-object-table v-if="objectResults.task.length > 0"
                                 v-bind:search-results="objectResults.task"
                                 v-bind:import-variables="taskVariables"
                                 v-bind:destination="'task'"
                                 v-bind:root-url="rootUrl"
            ></render-object-table>
            
            <!-- Kanban Cards -->
            <render-object-table v-if="objectResults.card.length > 0"
                                 v-bind:search-results="objectResults.card"
                                 v-bind:import-variables="cardVariables"
                                 v-bind:destination="'card'"
                                 v-bind:root-url="rootUrl"
            ></render-object-table>
            
            
            <!-- If there are no objects -->
            <div v-if="countObjects === 0 && isLoaded"
                 class="alert alert-primary"
            >
                It looks like no one has assigned you any tasks.
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    // Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    //Components
    import RenderObjectTable from "../render/RenderObjectTable.vue";

    export default {
        name: "DashboardMyObjects",
        components: {
            RenderObjectTable,
        },
        props: {
            rootUrl: {
                type: String,
                default: '/',
            },
        },
        data() {
            return {
                isLoaded: false,
                objectResults: {
                    'card': [],
                    'requirement': [],
                    'project': [],
                    'task': [],
                },
                cardVariables: {
                    header: 'Cards',
                    prefix: 'Card',
                    id: 'kanban_card_id',
                    title: 'kanban_card_text',
                    status: 'kanban_column__kanban_column_name',
                    end_date: '',
                },
                projectVariables: {
                    header: 'Projects',
                    prefix: 'Pro',
                    id: 'project_id',
                    title: 'project_name',
                    status: 'project_status',
                    end_date: 'project_end_date',
                },
                requirementVariables: {
                    header: 'Your Requirements',
                    prefix: 'Req',
                    id: 'requirement_id',
                    title: 'requirement_title',
                    status: 'requirement_status__requirement_status',
                    end_date: '',
                },
                taskVariables: {
                    header: 'Tasks',
                    prefix: 'Task',
                    id: 'task_id',
                    title: 'task_short_description',
                    status: 'task_status',
                    end_date: 'task_end_date',
                },
            }
        },
        mixins: [
            errorModalMixin,
        ],
        methods: {
            getMyObjects: function() {
                //Use axios to get the objects assigned to me
                axios.post(
                    `${this.rootUrl}dashboard/get/my_objects/`,
                ).then(response => {
                    this.objectResults = response['data'];

                    //Update loading status
                    this.isLoaded = true;
                }).catch(error => {
                    this.showErrorModal(error, 'Dashboard My Objects');
                })
            },
        },
        computed: {
            countObjects: function() {
                return this.objectResults.requirement.length + 
                    this.objectResults.project.length +
                    this.objectResults.task.length + 
                    this.objectResults.card.length;
            },
        },
        mounted() {
            //Get the data we want
            this.getMyObjects()
        },
    }
</script>

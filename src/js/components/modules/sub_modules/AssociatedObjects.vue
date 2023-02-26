<template>
    <div>
        <h2><Icon v-bind:icon="icons.objectStorage"></Icon> Associated Objects</h2>
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
                        <tr v-for="project in projectResults"
                            :key="project.project_id"
                        >
                            <td>
                                <a v-bind:href="`${rootUrl}project_information/${project.project_id}/`">
                                    <p>{{project.project_name}}</p>
                                    <div class="spacer"></div>
                                    <p class="small-text">
                                        Project {{project.project_id}} -
                                        End Date:
                                        {{getFriendlyDate(project.project_end_date)}}
                                    </p>
                                </a>
                            </td>
                            <td>{{project.project_status}}</td>
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
                        <tr v-for="requirement in requirementResults"
                            :key="requirement.requirement_id"
                        >
                            <td>
                                <a v-bind:href="`${rootUrl}requirement_information/${requirement.requirement_id}/`">
                                    <p>{{requirement.requirement_title}}</p>
                                    <div class="spacer"></div>
                                    <p class="small-text">
                                        Requirement {{requirement.requirement_id}}
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
                        <tr v-for="task in taskResults"
                            :key="task.task_id"
                        >
                            <td>
                                <a v-bind:href="`${rootUrl}task_information/${task.task_id}/`">
                                    <p>{{task.task_short_description}}</p>
                                    <div class="spacer"></div>
                                    <p class="small-text">
                                        Task {{task.task_id}} -
                                        End Date:
                                        {{getFriendlyDate(task.task_end_date)}}
                                    </p>
                                </a>
                            </td>
                            <td>{{task.task_status}}</td>
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
    import axios from 'axios';
    import { Icon } from '@iconify/vue';

    //VueX
    import { mapGetters } from 'vuex';

    //Mixins
    import iconMixin from "../../../mixins/iconMixin";

    export default {
        name: "AssociatedObjects",
        components: {
            Icon,
        },
        props: {
            destination: {
                type: String,
                default: '',
            },
            locationId: {
                type: Number,
                default: 0,
            },
        },
        mixins: [
            iconMixin,
        ],
        data() {
            return {
                projectResults: [],
                requirementResults: [],
                taskResults: [],
            }
        },
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
            })
        },
        methods: {
            getAssociatedObjectResults: function() {
                axios.post(
                    `${this.rootUrl}object_data/${this.destination}/${this.locationId}/associated_objects/`,
                ).then(response => {
                    this.projectResults = response.data.project;
                    this.requirementResults = response.data.requirement;
                    this.taskResults = response.data.task;
                }).catch(error => {
                    
                })
            },
            getFriendlyDate: function(input_date) {
                var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
                    local_date = new Date(input_date);

                return local_date.toLocaleString("en-US",options);
            }
        },
        mounted() {
            //Wait 200ms
            setTimeout(() => {
                this.getAssociatedObjectResults();
            }, 200);
        }
    }
</script>

<style scoped>

</style>
<template>
    <div>
        <div class="card">
            <div class="card-body">
                <!-- HEADING -->
                <h1>Search</h1>
                <hr>

                <!-- SEARCH FIELD -->
                <div class="form-row">
                    <div class="form-group">
                        <label>Search:</label>
                        <input type="text"
                               class="form-control search-organisation"
                               v-model="searchModel"
                        >
                    </div>
                    <div class="form-group">
                        <input type="checkbox"
                               id="inlcudeClosedObjects"
                               v-model="includeClosedObjectsModel"
                        >
                        <label for="inlcudeClosedObjects"> Include Closed Objects</label>
                    </div>
                </div>
            </div>
        </div>
        <br/>

        <!-- REQUIREMENTS RESULTS -->
        <list-search-results v-if="localSearchResults['requirement'].length > 0"
                             v-bind:search-results="localSearchResults['requirement']"
                             v-bind:import-variables="requirementVariables"
                             v-bind:destination="'requirement'"
        ></list-search-results>

        <!-- PROJECT RESULTS -->
        <list-search-results v-if="localSearchResults['project'].length > 0"
                             v-bind:search-results="localSearchResults['project']"
                             v-bind:import-variables="projectVariables"
                             v-bind:destination="'project'"
        ></list-search-results>

        <!-- TASK RESULTS -->
        <list-search-results v-if="localSearchResults['task'].length > 0"
                             v-bind:search-results="localSearchResults['task']"
                             v-bind:import-variables="taskVariables"
                             v-bind:destination="'task'"
        ></list-search-results>

        <!-- WHEN THERE ARE NO RESULTS -->
        <div v-if="localSearchResults['requirement'].length + localSearchResults['project'].length + localSearchResults['task'].length == 0"
             class="alert alert-warning"
        >
            Sorry - but there are no results for this search term. Please try searching for a different search term.
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    export default {
        name: "SearchObjects",
        props: {
            includeClosed: {
                Boolean,
            },
            searchInput: {
                String,
                required: false,
            },
            searchResults: {
                Array,
                required: true,
            },
        },
        data() {
            return {
                includeClosedObjectsModel: this.includeClosed,
                localSearchResults: this.searchResults,
                projectVariables: {
                    header: 'Projects',
                    prefix: 'Pro',
                    id: 'project_id',
                    title: 'project_name',
                    status: 'project_status',

                },
                requirementVariables: {
                    header: 'Requirements',
                    prefix: 'Req',
                    id: 'requirement_id',
                    title: 'requirement_title',
                    status: 'requirement_status__requirement_status',
                },
                searchModel: this.searchInput,
                searchTimeout: '',
                taskVariables: {
                    header: 'Tasks',
                    prefix: 'Task',
                    id: 'task_id',
                    title: 'task_short_description',
                    status: 'task_status',
                },
            }
        },
        methods: {
            getSearchResults: function() {
                // Setup the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('search',this.searchModel);
                data_to_send.set('include_closed',this.includeClosedObjectsModel);

                //Use axios to request data
                axios.post(
                    `/search/data/`,
                    data_to_send,
                ).then(response => {
                    //Update the localSearchResults with the data
                    this.localSearchResults = response['data'];
                }).catch(error => {
                    console.log("ERROR: ",error);
                })
            },
        },
        watch: {
            includeClosedObjectsModel: function() {
                //Stop the clock
                if (this.searchTimeout != '') {
                    //Stop the clock!
                    clearTimeout(this.searchTimeout);
                }

                //Get the search results - we don't need to wait for this case
                this.getSearchResults();
            },
            searchModel: function() {
                // Make sure the timer isn't running
                if (this.searchTimeout != '') {
                    //Stop the clock!
                    clearTimeout(this.searchTimeout);
                }

                //Set the search Timout
                this.searchTimeout = setTimeout(
                    this.getSearchResults,
                    500,
                )
            },
        },
        mounted() {
            //If the include closed is undefined - then we want to define it
            if (this.includeClosed == undefined) {
                this.includeClosedObjectsModel = false;
            }
        }
    }
</script>

<style scoped>

</style>
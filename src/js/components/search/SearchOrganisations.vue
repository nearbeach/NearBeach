<template>
    <div class="card">
        <div class="card-body">
            <!-- HEADING -->
            <h1>Search Organisations</h1>
            <br/>

            <!-- SEARCH FIELD -->
            <div class="form-group">
                <label>Search:</label>
                <input type="text"
                       class="form-control search-organisation"
                       v-model="searchModel"
                >
            </div>
            <hr>
            <list-organisations v-bind:organisation-results="localOrganisationResults"
            ></list-organisations>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    export default {
        name: "SearchOrganisations",
        props: [
            'organisationResults'
        ],
        data() {
            return {
                localOrganisationResults: this.organisationResults,
                searchModel: '',
                searchTimeout: '',
            }
        },
        methods: {
            getSearchResults: function() {
                //Create the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('search',this.searchModel);

                //Use axios to obtain the data we require
                axios.post(
                    '/search/organisation/data/',
                    data_to_send
                ).then(response => {
                    this.localOrganisationResults = response['data'];
                }).catch(error => {
                    console.log("Error: ",error);
                });
            },
        },
        watch: {
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
        }
    }
</script>

<style scoped>

</style>
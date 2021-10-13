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

            <!-- LIST OUT SEARCH RESULTS -->
            <hr>
            <list-organisations v-bind:organisation-results="localOrganisationResults"
                                v-bind:root-url="rootUrl"
                                v-bind:static-url="staticUrl"
            ></list-organisations>

            <!-- SHOW IF NO RESULTS -->
            <div class="alert alert-warning"
                 v-if="localOrganisationResults.length == 0"
            >There are no organisations with the search parameters used. Please try again.</div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    //Import mixins
    import searchMixin from "../../mixins/searchMixin";

    export default {
        name: "SearchOrganisations",
        props: {
            organisationResults: Array,
            staticUrl: {
                type: String,
                default: "/",
            },
            rootUrl: {
                type: String,
                default: "/",
            },
        },
        mixins: [
            searchMixin,
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
                    
                });
            },
        },
        watch: {
            searchModel: function() {
                this.searchTrigger({
                   'return_function': this.getSearchResults,
                   'searchTimeout': this.searchTimeout,
                });
            },
        }
    }
</script>

<style scoped>

</style>

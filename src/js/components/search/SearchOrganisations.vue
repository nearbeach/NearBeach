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
            ></list-organisations>

            <!-- SHOW IF NO RESULTS -->
            <div class="alert alert-warning"
                 v-if="localOrganisationResults.length === 0"
            >There are no organisations with the search parameters used. Please try again.</div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    //Import mixins
    import searchMixin from "../../mixins/searchMixin";

    //Vue Components
    import ListOrganisations from "../organisations/ListOrganisations.vue";

    export default {
        name: "SearchOrganisations",
        components: {
            ListOrganisations,
        },
        props: {
            organisationResults: {
                type: Array,
                default: () => {
                    return [];
                }
            },
            rootUrl: {
                type: String,
                default: '/',
            },
            staticUrl: {
                type: String,
                default: '/',
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
                    `${this.rootUrl}search/organisation/data/`,
                    data_to_send
                ).then(response => {
                    this.localOrganisationResults = response.data;
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
        },
        mounted() {
            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
                staticUrl: this.staticUrl,
            });
        }
    }
</script>

<style scoped>

</style>

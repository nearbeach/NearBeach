<template>
    <div class="card">
        <div class="card-body">
            <!-- Search bar and heading -->
            <h1>Search Permission Sets</h1>
            <br>
            <div class="form-group">
                <label>Search:</label>
                <input class="form-control search-groups"
                       v-model="searchModel"
                >
            </div>
            <hr>

            <!-- Search Results -->
            <div class="list-group"
                 v-if="permissionSetList.length > 0"
            >
                <a class="list-group-item list-group-item-action"
                   v-for="permissionSet in permissionSetList"
                   v-bind:href="`/permission_set_information/${permissionSet['pk']}/`"
                >
                    <strong>{{permissionSet['fields']['permission_set_name']}}</strong>
                    <br>
                </a>
            </div>

            <div class="alert alert-warning"
                 v-else
            >Sorry, there are no permission sets.</div>

            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="/new_group/"
                       class="btn btn-primary save-changes">
                        Add new Group
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    // Import mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import searchMixin from "../../mixins/searchMixin";

    export default {
        name: "SearchPermissionSets",
        props: {
            permissionSetResults: Array,
        },
        mixins: [
            errorModalMixin,
            searchMixin,
        ],
        data() {
            return {
                permissionSetList: this.permissionSetResults,
                searchModel: '',
                searchTimeout: '',
            }
        },
        methods: {
            getSearchResults: function() {
                //Setup data_to_send
                const data_to_send = new FormData();
                data_to_send.set('search', this.searchModel);

                //Use Axios to send data
                axios.post(
                    `/search/permission_set/data/`,
                    data_to_send,
                ).then(response => {
                    this.permissionSetList = response['data'];
                }).catch(error => {
                    //Show error
                    this.showErrorModal(error,'Search Permission Set','')
                })
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
    }
</script>

<style scoped>

</style>
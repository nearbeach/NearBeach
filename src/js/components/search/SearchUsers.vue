<template>
    <div class="card">
        <div class="card-body">
            <!-- Search bar and heading -->
            <h1>Search Groups</h1>
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
                 v-if="userList.length > 0"
            >
                <a class="list-group-item list-group-item-action"
                   v-for="user in userList"
                   v-bind:key="user.username"
                   v-bind:href="`/user_information/${user.id}/`"
                >
                    <strong>
                        {{user.username}}: {{user.first_name}} {{user.last_name}}
                    </strong>
                    <div class="spacer"></div>
                    <p class="small-text">{{user.email}}</p>
                </a>
            </div>

            <div class="alert alert-warning"
                 v-else
            >Sorry, there are no groups.</div>

            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a v-bind:href="`${rootUrl}new_user/`"
                       class="btn btn-primary save-changes">
                        Add new User
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
        name: "SearchUsers",
        props: {
            userResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            rootUrl: {
                type: String,
                default: '/',
            }
        },
        mixins: [
            errorModalMixin,
            searchMixin,
        ],
        data() {
            return {
                searchModel: '',
                searchTimeout: '',
                userList: this.userResults,
            }
        },
        methods: {
            getSearchResults: function() {
                //Setup data_to_send
                const data_to_send = new FormData();
                data_to_send.set('search', this.searchModel);

                //Use Axios to send data
                axios.post(
                    `${this.rootUrl}search/user/data/`,
                    data_to_send,
                ).then(response => {
                    this.userList = response.data;
                }).catch(error => {
                    //Show error
                    this.showErrorModal(error,'Search Users','')
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

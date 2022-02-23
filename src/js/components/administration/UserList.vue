<template>
    <div class="card">
        <div class="card-body">
            <h2>User List</h2>
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>List of Users</strong>
                    <p text="text-instructions">
                        The following are a list of users associated to INSERT DESTINATION. To add a new user please
                        click on the "Add User" at the bottom of the page.
                    </p>
                </div>
                <div class="col-md-8">
                    <table class="table">
                        <thead>
                            <tr>
                                <td>User</td>
                                <td>Group List</td>
                                <td>Permission List</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in uniqueListOfUsers">
                                <td>{{user['first_name']}} {{user['last_name']}}</td>
                                <td>{{getList(user['username'],'group__group_name')}}</td>
                                <td>{{getList(user['username'],'permission_set__permission_set_name')}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <hr>
            <div class="row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="addUser"
                    >Add User</a>
                </div>
            </div>
        </div>

        <!-- MODALS -->
        <admin-add-user v-bind:destination="destination"
                        v-bind:location-id="locationId"
        ></admin-add-user>
    </div>
</template>

<script>
    import {Modal} from 'bootstrap';

    //Import mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    //Vue Components
    import AdminAddUser from "./AdminAddUser.vue";

    export default {
        name: "UserList",
        components: {
            AdminAddUser,
        },
        props: {
            destination: {
                type: String,
                default: "",
            },
            locationId: {
                type: Number,
                default: 0,
            },
            userListResults: {
                type: Array, 
                default: function() { 
                    return []; 
                }, 
            },
        },
        data() {
            return {
                uniqueListOfUsers: [],
            }
        },
        methods: {
            addUser: function() {
                //Show the user's modal
                const addUserModal = new Modal(document.getElementById('addUserModal'))
                addUserModal.show();
            },
            getList: function(username, field) {
                //Filter the data for all username
                const filtered_user = this.userListResults.filter(row => {
                    return row['username'] == username;
                });

                //Map out the unique results we want
                const mapped_results = [...new Set(filtered_user.map(row => row[field]))];

                //Return the data
                return mapped_results;
            },
            getUniqueListOfUsers: function() {
                //Use map functionality to pull out fields we only interested in
                const mapped_results = this.userListResults.map(row => {
                    return {
                        'username': row['username'],
                        'first_name': row['username__first_name'],
                        'last_name': row['username__last_name'],
                        'email': row['email'],
                    };
                });

                //A simple for loop to extract out the unique usernames
                var unique_list_of_users = [];
                mapped_results.forEach(row => {
                    //Find out if the username already exists in the unique_list_of_users
                    const count_exists = unique_list_of_users.filter(unique_row => {
                        //If there exists the same username
                        return unique_row['username'] === row['username'];
                    }).length;

                    //If the count_exists is 0, it means it does not exist in the unique list. Add it
                    if (count_exists === 0) {
                        unique_list_of_users.push(row);
                    }
                });

                this.uniqueListOfUsers = unique_list_of_users;
            },
        },
        mounted() {
            //Obtain a unique list of users
            this.getUniqueListOfUsers();
        }
    }
</script>

<style scoped>

</style>
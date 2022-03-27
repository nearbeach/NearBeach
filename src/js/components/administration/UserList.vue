<template>
    <div class="card">
        <div class="card-body">
            <h2>User List</h2>
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>List of Users</strong>
                    <p text="text-instructions">
                        The following are a list of users associated to {{destination}}. To add a new user please
                        click on the "Add User" at the bottom of the page.
                    </p>
                </div>
                <div class="col-md-8">
                    <table class="table">
                        <thead>
                            <tr>
                                <td v-if="destination !== 'user'">User</td>
                                <td v-if="destination !== 'group'">Group List</td>
                                <td v-if="destination !== 'permission_set'">Permission List</td>
                                <td>Team Leader</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in uniqueListOfUsers"
                                :key="user.username"
                            >
                                <td v-if="destination !== 'user'">
                                    {{user['first_name']}} {{user['last_name']}}
                                </td>
                                <td v-if="destination !== 'group'">
                                    {{getList(user['username'],'group__group_name')}}
                                </td>
                                <td v-if="destination !== 'permission_set'">
                                    <span v-for="(permission_set, index) in getList(user['username'],'permission_set__permission_set_name')"
                                          :key="permission_set"
                                    >
                                        {{ index === 0 ? "": ", " }}{{permission_set}}
                                    </span>
                                </td>
                                <td style="text-align: center">
                                    <input class="form-check-input"
                                           type="checkbox"
                                           v-bind:checked="isTeamLeader(user['username'])"
                                           v-on:change="updateGroupLeader(user['username'], $event)"
                                           id="flexCheckDefault"
                                    >
                                </td>
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
    const axios = require('axios');

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
            isTeamLeader: function(username /* As an ID*/) {
                //Get count of the data from userListResults, where username and group_leader == true
                const count = this.userListResults.filter(row => {
                    return row.username === username && row.group_leader;
                }).length;

                //If length > 0, return true
                return count > 0;
            },
            updateGroupLeader: function(username, event) {
                //Get if the checkbox is ticked or not
                const group_leader = event.target.checked;

                //Send to the backend
                const data_to_send = new FormData();
                data_to_send.set('group_leader', group_leader);
                data_to_send.set('username', username);

                //If the destination is groups - we want to get the current group status
                //If the destination is permission sets - we want to get the current permission set status
                if (this.destination === "group") {
                    let group_data = this.getList(username,'group')
                    data_to_send.set('group', group_data[0]);
                } else if(this.destination === "permission_set") {
                    let permission_set = this.getList(username, 'permission_set');
                    data_to_send.set('permission_set', permission_set[0]);
                }

                axios.post(
                    `/update_group_leader_status/${this.destination}/`,
                    data_to_send,
                )
            }
        },
        mounted() {
            //Obtain a unique list of users
            this.getUniqueListOfUsers();
        }
    }
</script>

<style scoped>

</style>
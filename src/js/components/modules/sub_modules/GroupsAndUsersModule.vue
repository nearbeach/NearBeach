<template>
    <div>
        <!-- GROUPS -->
        <h2><i data-feather="grid"></i> Groups</h2>
        <p class="text-instructions">
            The following list are all the Groups connected to this {{destination}}. Users will have to be included
            in these groups to be added to this {{destination}}
        </p>
        <table class="table group-and-user-table">
            <thead>
                <tr>
                    <td>Group Name</td>
                </tr>
            </thead>
            <tbody>
                <tr v-for="group in groupList">
                    <td>{{ group['fields']['group_name'] }}</td>
                </tr>
            </tbody>
        </table>

        <!-- ADD GROUP -->
        <!-- TO DO - limit it to certain users -->
        <div class="row submit-row">
            <div class="col-md-12">
                <a href="javascript:void(0)"
                   class="btn btn-primary save-changes"
                   v-on:click="addNewGroup"
                >Add Group to {{destination}}</a>
            </div>
        </div>
        <hr>

        <!-- USERS -->
        <h2><i data-feather="users"></i> Users</h2>
        <p class="text-instructions">
            The following are a list of users who are connected to this {{destination}}. Please note - users have to be
            a part of the groups list above.
        </p>
        <div v-if="userList.length==0" class="alert alert-dark">
            Sorry - there are no current users active.
        </div>
        <div v-else>
            <table class="table user-table-module">
                <thead>
                    <tr>
                        <td style="width: 10px;"></td>
                        <td>User</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in userList">
                        <td>
                            <img src="/static/NearBeach/images/placeholder/people_tax.svg" alt="default profile" class="default-user-profile" />
                        </td>
                        <td>
                            <strong>{{user['fields']['username']}}: </strong>{{user['fields']['first_name']}} {{user['fields']['last_name']}}
                            <div class="spacer"></div>
                            <p class="user-card-email">
                                {{user['fields']['email']}}
                            </p>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- ADD GROUP -->
        <!-- TO DO - limit it to certain users -->
        <div class="row submit-row">
            <div class="col-md-12">
                <a href="javascript:void(0)"
                   class="btn btn-primary save-changes"
                   v-on:click="addNewUser"
                >Add User to {{destination}}</a>
            </div>
        </div>

        <!-- MODALS -->
        <!-- ADD GROUPS WIZARD -->
        <add-group-wizard v-bind:destination="destination"
                          v-bind:location-id="locationId"
                          v-on:update_group_list="updateGroupList($event)"
        ></add-group-wizard>

        <!-- ADD USER WIZARD -->
        <add-user-wizard v-bind:destination="destination"
                         v-bind:location-id="locationId"
                         v-bind:refresh-user-list="refreshUserListBoolean"
                         v-on:update_user_list="updateUserList($event)"
                         v-on:reset_refresh_user_list="resetRefreshUserList($event)"
        ></add-user-wizard>

    </div>
</template>

<script>
    //JavaScript extras
    const axios = require('axios');
    import {Modal} from "bootstrap";

    export default {
        name: "GroupsAndUsersModule",
        props: [
            'destination',
            'locationId',
        ],
        data() {
            return {
                groupList: [],
                refreshUserListBoolean: false,
                userList: [],
            }
        },
        methods: {
            addNewGroup: function() {
                var addGroupModal = new Modal(document.getElementById('addGroupModal'));
                addGroupModal.show();
            },
            addNewUser: function() {
                var addUserModal = new Modal(document.getElementById('addUserModal'));
                addUserModal.show();
            },
            getGroupList: function() {
                //Get the data from the database
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/group_list/`,
                ).then(response => {
                    this.groupList = response['data'];
                }).catch(error => {
                    console.log("Error: ",error);
                })
            },
            getUserList: function() {
                //Get the data from the database
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/user_list/`,
                ).then(response => {
                    this.userList = response['data'];
                }).catch(error => {
                    console.log("Error: ",error);
                });
            },
            resetRefreshUserList: function() {
                this.refreshUserListBoolean = false;
            },
            updateGroupList: function(data) {
                //Clear the group list
                this.groupList = data;

                //Now update the list of potential users
                this.refreshUserListBoolean = true;
            },
            updateUserList: function(data) {
                //Loop throught the data array and add each line item
                data.forEach(row => {
                    this.userList.push(row);
                });
            }

        },
        mounted() {
            this.getGroupList();
            this.getUserList();
        }
    }
</script>

<style scoped>

</style>
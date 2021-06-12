<template>
    <div>
        <!-- GROUPS -->
        <h2><IconifyIcon v-bind:icon="icons.groupPresentation"></IconifyIcon> Groups</h2>
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
        <h2><IconifyIcon v-bind:icon="icons.userIcon"></IconifyIcon> Users</h2>
        <p class="text-instructions">
            The following are a list of users who are connected to this {{destination}}. Please note - users have to be
            a part of the groups list above.
        </p>
        <div v-if="userList.length==0" class="alert alert-dark">
            Sorry - there are no current users active.
        </div>
        <div v-else
             class="user-card-layouts"
        >
            <div v-for="user in userList" 
                 class="user-card">
                <img src="/static/NearBeach/images/placeholder/people_tax.svg" alt="default profile" class="default-user-profile" />
                <div class="user-details">
                    <strong>{{user['first_name']}} {{user['last_name']}}</strong><br/>
                    {{user['username']}}
                    <div class="spacer"></div>
                    {{user['email']}}
                </div>
            </div>
        </div>

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
    import errorModalMixin from "../../../mixins/errorModalMixin";
    import iconMixin from "../../../mixins/iconMixin";

    const axios = require('axios');
    import {Modal} from "bootstrap";

    export default {
        name: "GroupsAndUsersModule",
        props: [
            'destination',
            'locationId',
        ],
        mixins: [
            errorModalMixin,
            iconMixin,
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
                    this.showErrorModal(error, this.destination);
                })
            },
            getUserList: function() {
                //Get the data from the database
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/user_list/`,
                ).then(response => {
                    this.userList = response['data'];
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
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
                // data.forEach(row => {
                //     this.userList.push(row);
                // });
                this.userList = data;
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

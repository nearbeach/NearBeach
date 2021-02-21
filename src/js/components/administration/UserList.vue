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
    </div>
</template>

<script>
    export default {
        name: "UserList",
        props: {
            destination: String,
            locationId: Number,
            userListResults: Array,
        },
        data() {
            return {
                uniqueListOfUsers: [],
            }
        },
        methods: {
            addUser: function() {
                //ADD CODE
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

                //User the Set functionality to create unique set
                this.uniqueListOfUsers = [...new Set(mapped_results)];
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
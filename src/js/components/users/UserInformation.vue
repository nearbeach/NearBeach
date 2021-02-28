<template>
    <div class="card">
        <div class="card-body">
            <h1>User Information</h1>
            <hr>

            <!-- USERNAME -->
            <div class="row">
                <div class="col-md-4">
                    <strong>UserName</strong>
                    <p class="text-instructions">
                        The username is set and can not be changed from this location. If you need to change the
                        username, please go to the Django Admin Panel.
                    </p>
                    <p class="text-instructions">
                        The ID is the primary key assigned to the username. This can not be edited. It can be ignored.
                    </p>
                </div>
                <div class="col-md-8">
                    <strong>Username:</strong> {{userResults[0]['fields']['username']}}
                    <strong> | ID:</strong> {{userResults[0]['pk']}}
                </div>
            </div>

            <!-- USER DETAILS -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>User Details</strong>
                    <p class="text-instructions">
                        Please fill out the user details.
                    </p>
                </div>
                <div class="col-md-8">
                    <div class="row">
                        <div class="col-md-6">
                            <label>First Name:</label>
                            <input type="text"
                                   v-model="firstNameModel"
                                   class="form-control"
                            >
                        </div>
                        <div class="col-md-6">
                            <label>Last Name:</label>
                            <input type="text"
                                   v-model="lastNameModel"
                                   class="form-control"
                            >
                        </div>
                        <div class="col-md-6">
                            <label>Email:</label>
                            <input type="email"
                                   v-model="emailModel"
                                   class="form-control"
                            >
                        </div>
                    </div>
                </div>
            </div>
            <hr>

            <!-- Active USER -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Active User</strong>
                    <p class="text-instructions">
                        Untick this option if the user is no longer active.
                    </p>
                </div>
                <div class="col-md-8">
                    <label>Is User Active? </label>
                    <input type="checkbox"
                           v-model="isActiveModel"
                    >
                </div>
            </div>
            <hr>

            <!-- User is SUPER -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Is User a Superuser</strong>
                    <p class="text-instructions">
                        Tick this functionality if you would like the user to gain access to the /admin/ functionality.
                        This is not recommended for anyone outside of an IT team.
                    </p>
                </div>
                <div class="col-md-8">
                    <label>Is User a Superuser? </label>
                    <input type="checkbox"
                           v-model="isSuperuserModel"
                    >
                </div>
            </div>
            <hr>

            <!-- UPDATE USER -->
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateUser"
                    >
                        Update User Details
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "UserInformation",
        props: {
            userResults: Array,
        }
    }
</script>

<style scoped>

</style>
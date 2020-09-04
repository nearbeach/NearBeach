<template>
    <div class="modal fade" id="addUserModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="users"></i> Add User Wizard</h2>
                    <button type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            id="addUserCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div v-if="userFixList > 0"
                         class="row">
                        <div class="col-md-4">
                            <strong>Add Users</strong>
                            <p class="text-instructions">
                                Use the following multiple select to select which users you want to add to this
                                {{destination}}.
                            </p>
                            <p class="text-instructions">
                                Please note: A user's group has to be added to the {{destination}} before the user
                                can be added.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <v-select :options="userFixList"
                                      v-model="userModel"
                            ></v-select>
                        </div>
                    </div>
                    <div v-else
                         class="row"
                    >
                        <div class="col-md-6">
                            <strong>Sorry - no results</strong>
                            <p class="text-instructions">
                                This could be because
                                <ul>
                                    <li>There are no more users left to add</li>
                                    <li>
                                        The user you are after is in a group not current added to this {{destination}}
                                    </li>
                                </ul>
                            </p>
                        </div>
                        <div class="col-md-6 no-search">
                            <img src="/static/NearBeach/images/placeholder/questions.svg" alt="Sorry - there are no results" />
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button"
                            class="btn btn-secondary"
                            data-dismiss="modal"
                    >Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-bind:disabled="userModel.length==0"
                    >Add User(s)</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "AddUserWizard",
        props: [
            'destination',
            'locationId',
        ],
        data() {
            return {
                userFixList: [],
                userModel: [],
            }
        },
        methods: {
            getUserList: function() {
                //ADD CODE
            }
        },
        mounted() {
            this.getUserList();
        },
    }
</script>

<style scoped>

</style>
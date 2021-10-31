<template>
    <div class="card">
        <div class="card-body">
            <h1>New Group</h1>
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <strong>Create a new group</strong>
                    <p class="text-instructional">
                        Each group should contain a unique name. If the name already exists then we won't be able
                        to create the group.
                    </p>
                </div>
                <div class="col-md-8">
                    <div class="form-group">
                        <label>
                            Group Name
                            <span class="error"
                                  v-if="!$v.groupNameModel.required && $v.groupNameModel.$dirty"
                            >
                                Please suppy a title.
                            </span>
                            <span class="error" v-if="!uniqueGroupName"> Please supply a unique name</span>
                            <span class="error" v-if="checkingGroupName"> Checking group name...</span>
                        </label>
                        <input class="form-control"
                               v-model="groupNameModel"
                        >
                    </div>

                    <div class="form-group">
                        <label>
                            Parent Group (optional)
                        </label>
                        <v-select :options="groupResultsFixList"
                                  v-model="parentGroupModel"
                                  label="group_name"
                                  class="form-control"
                        />
                    </div>
                </div>
            </div>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="addNewGroup"
                    >Create new Group</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios')

    // Validation
    import { required } from 'vuelidate/lib/validators';

    // Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import searchMixin from "../../mixins/searchMixin";

    export default {
        name: "NewGroup",
        props: {
            groupResults: {
                type: Array,
                default: function() {
                    return [];
                },
            },
        },
        data() {
            return {
                checkingGroupName: false,
                groupNameModel: '',
                groupResultsFixList: [],
                parentGroupModel: '',
                uniqueGroupName: true,
            }
        },
        mixins: [
            errorModalMixin,
            searchMixin,
        ],
        validations: {
            groupNameModel: {
                required,
            },
        },
        watch: {
            groupNameModel: function() {
                // Tell user that we are searching for the group name
                this.checkingGroupName = true;

                // Apply the search functional mixing
                this.searchTrigger({
                    'return_function': this.checkGroupName,
                    'searchTimeout': this.searchTimeout,
                });
            },
        },
        methods: {
            addNewGroup: function() {
                //Check to make sure everythign is validated
                this.$v.$touch();

                if (this.$v.$invalid || !this.uniqueGroupName) {
                    //The group name is not valid, or is not unique. Show error and return
                    this.showValidationErrorModal();

                    //Just return
                    return;
                }

                //Get the data
                const data_to_send = new FormData();
                data_to_send.set('group_name', this.groupNameModel);

                if (this.parentGroupModel['value'] !== undefined) {
                    data_to_send.set('parent_group', this.parentGroupModel['value']);
                }

                //Use Axios to send data
                axios.post(
                    `/new_group/save/`,
                    data_to_send,
                ).then(response => {
                    //Go to that webpage
                    window.location.href = response['data'];
                }).catch(error => {
                    this.showErrorModal(error, 'New Group', '');
                });
            },
            checkGroupName: function() {
                //Send group name to backend to make sure it is not a duplicate
                const data_to_send = new FormData();
                data_to_send.set('search', this.groupNameModel);

                //User Axios to send data
                axios.post(
                    `/group_information/check_group_name/`,
                    data_to_send,
                ).then(response => {
                    // Update the uniqueGroupName
                    this.uniqueGroupName = response['data'].length == 0;

                    // Hide the checking group name
                    this.checkingGroupName = false;
                }).catch(error => {
                    this.showErrorModal(error,'New Group','');
                })
            },
        },
        mounted() {
            //This will map reconstruct the JSON data into a V-SELECT friendly data
            this.groupResultsFixList = this.groupResults.map(row => {
                return {
                    'group_name': row['fields']['group_name'],
                    'value': row['pk'],
                }
            });
        }
    }
</script>

<style scoped>

</style>

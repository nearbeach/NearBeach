<template>
    <div class="card">
        <div class="card-body">
            <h1>Group Information</h1>
            <hr>

            <div class="row">
                <div class="col-md-4">
                    <strong>Group Information</strong>
                    <p class="text-instruction">
                        Please edit the group information here. Please note - groups have to be unique!
                    </p>
                </div>
                <div class="col-md-8">
                    <div class="form-group">
                        <label>Group Name</label>
                        <input type="text"
                               v-model="groupNameModel"
                               class="form-control"
                        >
                    </div>
                    <div class="form-group">
                        <label>Parent Group</label>
                        <v-select :options="parentGroupFixList"
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
                       v-on:click="updateGroup"
                    >Update Group</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    //Load mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    export default {
        name: "GroupInformation",
        props: {
            groupResults: Array,
            parentGroupResults: Array,
        },
        data() {
            return {
                groupNameModel: this.groupResults[0]['fields']['group_name'],
                parentGroupFixList: [],
                parentGroupModel: '',
            }
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
        methods: {
            updateGroup: function() {
                //Construct data to send
                const data_to_send = new FormData();
                data_to_send.set('group_name', this.groupNameModel);

                //If there is a value in parent group - setup the data
                if (this.parentGroupResults['value'] !== undefined) {
                    data_to_send.set('parent_group', this.parentGroupModel['value']);
                }

                //Show the loading mixin
                this.showLoadingModal("Group Information")

                //User axios to send data
                axios.post(
                    `/group_information/${this.groupResults[0]['pk']}/save/`,
                    data_to_send,
                ).then(response => {
                    this.closeLoadingModal();
                }).catch(error => {
                    this.showErrorModal(error,'group_information', '');
                });
            },
        },
        mounted() {
            // Create the parent group fix list
            const parent_group_fix_list = this.parentGroupResults.map(row => {
                return {
                    'group_name': row['fields']['group_name'],
                    'value': row['pk'],
                }
            });


            // Get the parent object from the parent group fix list
            const parent_group = parent_group_fix_list.filter(row => {
                return row['value'] === this.groupResults[0]['fields']['parent_group'];
            });

            //Set the variables
            this.parentGroupFixList = parent_group_fix_list;
            this.parentGroupModel = '';
            if (parent_group.length > 0) {
                this.parentGroupModel = parent_group[0];
            }
        }
    }
</script>

<style scoped>

</style>
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
                        <label>Group Name</label>
                        <input class="form-control"
                               v-model="groupNameModel"
                        >
                    </div>
                </div>
            </div>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="submitNewGroup"
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
        props: {},
        data() {
            return {
                checkingGroupName: false,
                groupNameModel: '',
                isGroupNameUnique: false,
            }
        },
        validations: {
            groupNameModel: {
                required,
            },
        },
        watch: {
            groupNameModel: function() {

            },
        },
        methods: {
            checkGroupNameUnique: function() {

            },
            submitNewGroup: function() {

            },
        }
    }
</script>

<style scoped>

</style>
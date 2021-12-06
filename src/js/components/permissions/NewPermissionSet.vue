<template>
    <div class="card">
        <div class="card-body">
            <h1>New Permission Set</h1>
            <hr>

            <div class="row">
                <div class="col-md-4">
                    <strong>New Permission Set</strong>
                    <p class="text-instructions">
                        Please enter in a unique permission set name. Please note - all values are default permission
                        level of 0.
                    </p>
                </div>
                <div class="col-md-8">
                    <label>Permission Set Name</label>
                    <input type="text"
                           v-model="permissionSetNameModel"
                           class="form-control"
                    >
                </div>
            </div>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="addNewPermissionSet"
                    >Create new Permission Set</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    //Import mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    export default {
        name: "NewPermissionSet",
        props: {
            rootUrl: {
                type: String,
                default: '/',
            }
        },
        data() {
            return {
                permissionSetNameModel: '',
            }
        },
        mixins: [
            errorModalMixin,
        ],
        methods: {
            addNewPermissionSet: function() {
                //Data to send
                const data_to_send = new FormData();
                data_to_send.set('permission_set_name', this.permissionSetNameModel);

                axios.post(
                    `${rootUrl}new_permission_set/save/`,
                    data_to_send,
                ).then(response => {
                    //Go to the new location
                    window.location.href = response['data'];
                }).catch(error => {
                    this.showErrorModal(error, 'New Permission Set','');
                })
            }
        }
    }
</script>

<style scoped>

</style>
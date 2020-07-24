<template>
    <div class="card">
        <h1>New Requirement</h1>
        <hr>
        <div class="row">
            <!-- Description -->
            <div class="col-md-4">
                <h3>Description</h3>
                <p>Place a basic helicopter view of the requirement description here. You will be able to break this
                    description down into svaluemaller items using the requirement items below.</p>
            </div>

            <div class="col-md-8" style="min-height: 610px;">
                <div class="form-group">
                    <label for="id_requirement_title">Requirement Title</label>
                    <input id="id_requirement_title"
                           class="form-control"
                           name="requirement_title"
                           type="text"
                           required="true"
                           maxlength="255"
                           v-model="requirementTitleModel"
                    />
                </div>

                <br/>
                <div class="form-group">
                    <label>Requirement Scope</label><br>
                    <img src="static/NearBeach/images/placeholder/body_text.svg"
                         class="loader-image"
                    />
                    <editor
                       :init="{
                         height: 500,
                         menubar: false,
                         toolbar: 'undo redo | formatselect | ' +
                          'bold italic backcolor | alignleft aligncenter ' +
                          'alignright alignjustify | bullist numlist outdent indent | ',
                       }"
                       v-model="descriptionModel"
                    />
                </div>
            </div>
        </div>

        <!-- Stakeholder Organisation -->
        <hr>
        <get-stakeholders v-on:update_stakeholder_model="updateStakeholderModel($event)"></get-stakeholders>

        <!-- Status -->
        <hr>
        <div class="row">
            <div class="col-md-4">
                <h3>Status</h3>
                <p>Set the Requirement Status and Type here.</p>
            </div>
            <div class="col-md-4">
                <div class="form-group">
                    <label>Requirement Status</label>
                    <v-select :options="statusFixList"
                              label="status"
                              v-model="statusModel"
                    ></v-select>
                </div>

            </div>
            <div class="col-md-4">
                <div class="form-group">
                    <label>Requirement Type</label>
                    <v-select :options="typeFixList"
                              label="type"
                              v-model="typeModel"
                    ></v-select>
                </div>
            </div>
        </div>

        <!-- Group Permissions -->
        <hr>
        <group-permissions v-bind:group-results="groupResults"
                           v-on:update_group_model="updateGroupModel($event)"
        ></group-permissions>

        <!-- Submit Button -->
        <hr>
        <div class="row submit-row">
            <div class="col-md-12">
                <a href="javascript:void(0)"
                   class="btn btn-primary save-changes"
                   v-on:click="submitNewRequirement"
                >Create new Requirement</a>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript Libraries
    const axios = require('axios');
    import { Modal } from 'bootstrap';

    //Vue components
    import GetStakeholders from '../organisations/GetStakeholders.vue';
    import GroupPermissions from '../permissions/GroupPermissions.vue';

    export default {
        name: "NewRequirement",
        components: {
            axios,
            GetStakeholders,
            GroupPermissions,
        },
        props: [
            'statusList',
            'typeList',
            'groupResults',
        ],
        data() {
            return {
                descriptionModel: '',
                groupModel: '',
                requirementTitleModel: '',
                stakeholderModel: '',
                statusFixList: [],
                statusModel: '',
                typeFixList: [],
                typeModel: '',
            }
        },
        methods: {
            submitNewRequirement: function() {
                // Apply the loading screen to hide everything
                var loader_elem = document.getElementById("loader");
                loader_elem.style.transform = "translateY(0)";

                // Set up the data object to send
                const data_to_send = new FormData();
                data_to_send.set('requirement_title', this.requirementTitleModel);
                data_to_send.set('requirement_description',this.descriptionModel);
                data_to_send.set('stakeholder',this.stakeholderModel['value']);
                data_to_send.set('requirement_status',this.statusModel['value']);
                data_to_send.set('requirement_type',this.typeModel['value']);

                // Insert a new row for each group list item
                this.groupModel.forEach((row,index) => {
                    data_to_send.append(`group_list`,row['value']);
                });

                // Use Axion to send the data
                axios.post(
                        'new_requirement/save/',
                        data_to_send
                    ).then((response) => {
                        // Use the result to go to the url
                        window.location.href = response['data']
                    }).catch((error) => {
                        // Get the error modal
                        var elem_cont = document.getElementById("errorModalContent");

                        // Update the content
                        elem_cont.innerHTML = `<strong>HTML ISSUE:</strong> We could not save the new requirement<hr>${error}`;

                        // Show the modal
                        //var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
                        var errorModal = new Modal(document.getElementById('errorModal'));
                        errorModal.show();

                        // Hide the loader
                        loader_elem.style.transform = "translateY(-100vh)";
                    });
            },
            updateGroupModel: function(newGroupModel) {
                //Update the group model
                this.groupModel = newGroupModel;
            },
            updateStakeholderModel: function(newStakeholderModel) {
                this.stakeholderModel = newStakeholderModel;
            }
        },
        mounted() {
            //We need to extract "fields" array from the statusList/typeList json data
            this.statusList.forEach((row) => {
                //Construct the object
                var construction_object = {
                    'value': row['pk'],
                    'status': row['fields']['requirement_status'],
                };

                //Push the object to status fix list
                this.statusFixList.push(construction_object);
            });
            this.typeList.forEach((row) => {
                //Construct the object
                var construction_object = {
                    'value': row['pk'],
                    'type': row['fields']['requirement_type'],
                }

                //Push the object to type fix list
                this.typeFixList.push(construction_object);
            });
        },
    }
</script>

<style scoped>

</style>
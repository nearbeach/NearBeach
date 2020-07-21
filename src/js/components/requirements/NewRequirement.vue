<template>
    <div class="card">
        <h1>New Requirement</h1>
        <hr>
        <div class="grid-x">
            <!-- Description -->
            <div class="small-12 large-4">
                <h3>Description</h3>
                <p>Place a basic helicopter view of the requirement description here. You will be able to break this
                    description down into svaluemaller items using the requirement items below.</p>
            </div>

            <div class="small-12 large-8" style="min-height: 580px;">
                <label>Requirement Title
                    <input id="id_requirement_title"
                           name="requirement_title"
                           type="text"
                           required="true"
                           maxlength="255"
                           v-model="requirementTitleModel"
                    />
                </label>
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

            <!-- Stakeholder Organisation -->
            <hr>
            <div class="small-12 large-4">
                <h3>Stakeholder Organisation</h3>
                <p>Please search for your stakeholder organisation in the dropdown box. Once found, please select.</p>
            </div>
            <div class="small-12 large-8">
                <label>Stakeholder Organisation
                    <v-select :options="stakeholderFixList"
                              @search="fetchOptions"
                              v-model="stakeholderModel"
                              label="organisation_name"
                    />
                </label>
            </div>

            <!-- Status -->
            <hr>
            <div class="small-12 large-4">
                <h3>Status</h3>
                <p>Set the Requirement Status and Type here.</p>
            </div>
            <div class="small-12 large-4">
                <label>Requirement Status
                    <v-select :options="statusFixList"
                              label="status"
                              v-model="statusModel"
                    ></v-select>
                </label>
            </div>
            <div class="small-12 large-4">
                <label>Requirement Type
                    <v-select :options="typeFixList"
                              label="type"
                              v-model="typeModel"
                    ></v-select>
                </label>
            </div>

        </div>
        <!-- Group Permissions -->
        <hr>
        <group-permissions v-bind:group-results="groupResults"
                           v-on:update_group_model="updateGroupModel($event)"
        ></group-permissions>

        <!-- Submit Button -->
        <hr>
        <div class="cell medium-12 large-12">
            <a href="javascript:void(0)"
               class="button save-changes"
               v-on:click="submitNewRequirement"
            >Create new Requirement</a>
        </div>
    </div>
</template>

<script>
    //JavaScript Libraries
    const axios = require('axios');

    //jQuery
    import $ from 'jquery';

    //Vue components
    import GroupPermissions from '../permissions/GroupPermissions.vue';

    export default {
        name: "NewRequirement",
        components: {
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
                searchTimeout: '',
                stakeholderFixList: [],
                stakeholderModel: '',
                statusFixList: [],
                statusModel: '',
                typeFixList: [],
                typeModel: '',
            }
        },
        computed: {
            group_list_results: function() {
                // Declare the empty array
                var group_list = [];

                // Loop to extract the values we need
                this.groupModel.forEach((row) => {
                    group_list.push(row['value']);
                });

                console.log("RETURNING GROUP LIST: ",group_list);

                return group_list;
            }
        },
        methods: {
            getOrganisationData: function(search,loading) {
                // Save the seach data in FormData
                const data_to_send = new FormData();
                data_to_send.set('search',search);

                // Now that the timer has run out, lets use AJAX to get the organisations.
                axios.post(
                    'search/organisation/data/',
                    data_to_send
                ).then(response => {
                    //Clear the stakeholderFixList
                    this.stakeholderFixList = [];

                    //Extract the required JSON data
                    var extracted_data = response['data'];

                    //Look through the extracted data - and map the required fields into stakeholder fix list
                    extracted_data.forEach((row) => {
                        //Create the creation object
                        var creation_object = {
                            'value': row['pk'],
                            'organisation_name': row['fields']['organisation_name'],
                            'organisation_website': row['fields']['organisation_website'],
                            'organisation_email': row['fields']['organisation_email'],
                            'organisation_profile_picture': row['fields']['organisation_profile_picture'],
                        };

                        //Push that object into the stakeholders
                        this.stakeholderFixList.push(creation_object)
                    });
                }).catch(function (error) {
                    // Get the error modal
                    var elem_cont = document.getElementById("errorModalContent");

                    // Update the content
                    elem_cont.innerHTML = `<strong>Search Organisation Issue:</strong><br/>${error}`;

                    // Show the modal
                    var popup = new Foundation.Reveal($('#errorModal'));
                    popup.open();

                    // Hide the loader
                    var loader_element = document.getElementById("loader");
                    loader_element.style.display = "none";
                });
            },
            fetchOptions: function(search, loading) {
                // Make sure the timer isn't running
                if (this.searchTimeout != '') {
                    //Stop the clock!
                    clearTimeout(this.searchTimeout);
                }

                // Reset the clock, to only search if there is an uninterupted 0.5s of no typing.
                if (search.length >= 3) {
                    this.searchTimeout = setTimeout(
                        this.getOrganisationData,
                        500,
                        search,
                        loading
                    )
                }
            },
            submitNewRequirement: function() {
                // Apply the loading screen to hide everything
                var elem = document.getElementById("loader");
                elem.style.display = "";

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
                    ).then(function (response) {
                        // Use the result to go to the url
                        window.location.href = response['data']
                    }).catch(function (error) {
                        // Get the error modal
                        var elem_cont = document.getElementById("errorModalContent");

                        // Update the content
                        elem_cont.innerHTML = `<strong>HTML ISSUE:</strong>We could not save the new requirement<br/>${error}`;

                        // Show the modal
                        var popup = new Foundation.Reveal($('#errorModal'));
                        popup.open();

                        // Hide the loader
                        var loader_element = document.getElementById("loader");
                        loader_element.style.display = "none";
                    });
            },
            updateGroupModel: function(newGroupModel) {
                //Update the group model
                this.groupModel = newGroupModel;
            },
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
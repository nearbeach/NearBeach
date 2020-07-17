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

            <div class="small-12 large-8" style="min-height: 500px;">
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

            <!-- Group Permissions -->
            <hr>
            <group-permissions v-bind:group-results="groupResults"></group-permissions>

            <!-- Submit Button -->
            <hr>
            <div class="cell medium-12 large-12">
                <a href="javascript:void(0)"
                   class="button save-changes"
                   v-on:click="submitNewRequirement"
                >Create new Requirement</a>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript components
    import Editor from '@tinymce/tinymce-vue';
    import vSelect from "vue-select";

    const axios = require('axios');

    //Vue components
    import GroupPermissions from '../permissions/GroupPermissions.vue';

    export default {
        name: "NewRequirement",
        components: {
            Editor,
            vSelect,
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
        methods: {
            getOrganisationData: function(search,loading) {
                // Now that the timer has run out, lets use AJAX to get the organisations.
                axios({
                    method: 'POST',
                    url: 'search/organisation/data',
                    data: {
                        'id_search': search,
                }}).then(response => {
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
                    })
                    .catch(function (error) {
                        // handle error
                        console.log("THE HTML ERROR: ",error);
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
                //Get all the data stored in the modals and send it via ajax
                axios({
                    method: 'POST',
                    url: 'new_requirement/save/'
                    data: {
                        'id_requirement_title': this.requirementTitleModel,
                        'id_requirement_description': this.descriptionModel,
                        'id_stakeholder': this.stakeholderModel,
                        'id_requirement_status': this.statusModel,
                        'id_requirement_type': this.typeModel,
                        'id_group_list': "this.groupMo"
                    }
                }).then(

                )
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
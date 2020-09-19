<template>
    <div class="card">
        <div class="card-body">
            <h1>Requirement Information</h1>
            <hr>

            <div class="row">
                <!-- Description -->
                <div class="col-md-4">
                    <h2>Description</h2>
                    <p class="text-instructions">
                        Place a basic bird's eye view of the requirement description here. You will be able to break
                        the requirement down into smaller components called 'Items' below in the 'Requirement Item'
                        section.
                    </p>
                </div>

                <div class="col-md-8" style="min-height: 610px;">
                    <div class="form-group">
                        <label for="id_requirement_title">Requirement Title:
                            <span class="error" v-if="!$v.requirementTitleModel.required"> Please suppy a title.</span>
                        </label>
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
                    <label>Requirement Scope:
                        <span class="error" v-if="!$v.requirementScopeModel.required"> Please supply a scope.</span>
                        <span class="error" v-if="!$v.requirementScopeModel.maxLength"> Sorry - too many characters.</span>
                    </label><br>
                    <img src="/static/NearBeach/images/placeholder/body_text.svg"
                         class="loader-image"
                         alt="loading image for Tinymce"
                    />
                    <editor
                       :init="{
                         height: 500,
                         menubar: false,
                         toolbar: 'undo redo | formatselect | ' +
                          'bold italic backcolor | alignleft aligncenter ' +
                          'alignright alignjustify | bullist numlist outdent indent | ',
                       }"
                       v-model="requirementScopeModel"
                    />
                </div>
            </div>

            <!-- Stakeholder Information -->
            <hr>
            <div class="row">
                <!-- Description -->
                <div class="col-md-4">
                    <h2>Stakeholder</h2>
                </div>
                <div class="col-md-8 organisation-details">
                    <img v-bind:src="getStakeholderImage" alt="Stakeholder Logo" class="organisation-image">
                    <div class="organisation-name">
                        {{stakeholderModel['organisation_name']}}
                    </div>
                    <div class="organisation-link">
                        <i data-feather="external-link"></i> Website:
                        <a v-bind:href="stakeholderModel['organisation_website']" target="_blank">
                            {{ stakeholderModel['organisation_website'] }}
                        </a>
                    </div>
                    <div class="organisation-email">
                        <i data-feather="mail"></i> Email:
                        <a v-bind:href="`mailto:${stakeholderModel['organisation_email']}`">
                            {{stakeholderModel['organisation_email']}}
                        </a>
                    </div>
                </div>
            </div>

            <!-- Status -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <h2>Status</h2>
                    <p class="text-instructions">Set the Requirement Status and Type here.</p>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label>Requirement Status
                            <span class="error" v-if="!$v.statusModel.required && $v.statusModel.$dirty"> Please select a status.</span>
                        </label>
                        <v-select :options="statusFixList"
                                  label="status"
                                  v-model="statusModel"
                        ></v-select>
                    </div>

                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label>Requirement Type
                            <span class="error" v-if="!$v.typeModel.required && $v.typeModel.$dirty"> Please select a type.</span>
                        </label>
                        <v-select :options="typeFixList"
                                  label="type"
                                  v-model="typeModel"
                        ></v-select>
                    </div>
                </div>
            </div>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateRequirement"
                    >Update Requirement</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript Libraries
    import {Modal} from "bootstrap";

    const axios = require('axios');

    //Validation
    import { required, maxLength } from 'vuelidate/lib/validators';

    export default {
        name: "RequirementInformation",
        components: {},
        props: [
            'defaultStakeholderImage',
            'organisationResults',
            'requirementResults',
            'statusList',
            'typeList',
        ],
        data() {
            return {
                requirementScopeModel: '',
                requirementTitleModel: '',
                stakeholderModel: '',
                statusFixList: [],
                statusModel: '',
                typeFixList: [],
                typeModel: '',
            }
        },
        validations: {
            requirementScopeModel: {
                required,
                maxLength: maxLength(630000),
            },
            requirementTitleModel: {
                required
            },
            statusModel: {
                required
            },
            typeModel: {
                required
            },
        },
        methods: {
            updateRequirement: function() {
                // Check the validation first
                this.$v.$touch();

                if (this.$v.$invalid) {
                    //Show the error dialog and notify to the user that there were field missing.
                    var elem_cont = document.getElementById("errorModalContent");

                    // Update the content
                    elem_cont.innerHTML =
                        `<strong>FORM ISSUE:</strong> Sorry, but can you please fill out the form completely.`;

                    // Show the modal
                    var errorModal = new Modal(document.getElementById('errorModal'));
                    errorModal.show();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                //Open up the loading modal
                var loadingModal = new Modal(document.getElementById('loadingModal'));
                loadingModal.show();

                //Update message in loading modal
                document.getElementById("loadingModalContent").innerHTML = `Updating your Requirement details`;

                // Set up the data object to send
                const data_to_send = new FormData();
                data_to_send.set('requirement_title', this.requirementTitleModel);
                data_to_send.set('requirement_scope',this.requirementScopeModel);
                data_to_send.set('requirement_status',this.statusModel['value']);
                data_to_send.set('requirement_type',this.typeModel['value']);

                // Use Axion to send the data
                axios.post(
                    'save/',
                    data_to_send
                ).then(response => {
                    //Update the message in the loading modal
                    document.getElementById("loadingModalContent").innerHTML = `UPDATED SUCCESSFULLY`;

                    //Close after 1 second
                    setTimeout(() => {
                        loadingModal.hide();
                    },1000)
                }).catch((error) => {
                    //Hide the loading modal
                    loadingModal.hide();

                    // Get the error modal
                    var elem_cont = document.getElementById("errorModalContent");

                    // Update the content
                    elem_cont.innerHTML = `<strong>HTML ISSUE:</strong> We could not save the new requirement<hr>${error}`;

                    // Show the modal
                    var errorModal = new Modal(document.getElementById('errorModal'));
                    errorModal.show();
                });
            }
        },
        computed: {
            getStakeholderImage: function() {
                if (this.stakeholderModel['organisation_profile_picture'] == '') {
                    //There is no image - return the default image
                    return this.defaultStakeholderImage;
                }
                return this.stakeholderModel['organisation_profile_picture']
            }
        },
        mounted() {
            //Get data from the requirementResults and delegate to the Models
            var requirement_results = this.requirementResults[0]['fields'];

            this.requirementScopeModel = requirement_results['requirement_scope'];
            this.requirementTitleModel = requirement_results['requirement_title'];

            //Extract the organisation results directly
            this.stakeholderModel = this.organisationResults[0]['fields'];

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


            //Filter the status fix list to get the current model version
            this.statusModel = this.statusFixList.filter((row) => {
                return row['value'] == requirement_results['requirement_status'];
            })[0];

            this.typeModel = this.typeFixList.filter((row) => {
                return row['value'] == requirement_results['requirement_type'];
            })[0];
        }
    }
</script>

<style scoped>

</style>
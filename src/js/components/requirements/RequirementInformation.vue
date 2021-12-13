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
                    <img v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
                         class="loader-image"
                         alt="loading image for Tinymce"
                    />
                    <editor
                       :init="{
                         height: 500,
                         menubar: false,
                         plugins: 'lists',
                        toolbar: [
                           'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                           'bold italic strikethrough underline backcolor | ' +
                           'bullist numlist outdent indent | removeformat'
                        ]}"
                       v-bind:content_css="false"
                       v-bind:disabled="isReadOnly"
                       v-bind:skin="false"
                       v-model="requirementScopeModel"
                    />
                </div>
            </div>

            <!-- Stakeholder Information -->
            <hr>
            <stakeholder-information v-bind:organisation-results="organisationResults"
                                     v-bind:default-stakeholder-image="defaultStakeholderImage"
            ></stakeholder-information>

            <!-- Status -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <h2>Status</h2>
                    <p class="text-instructions">Set the Requirement Status and Type here.</p>
                </div>
                <div class="col-md-8">
                    <div class="col-md-12"
                         v-if="!statusModel['status_closed']"
                    >
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label>Requirement Status
                                        <span class="error" v-if="!$v.statusModel.required && $v.statusModel.$dirty"> Please select a status.</span>
                                    </label>
                                    <v-select :options="statusFixList"
                                              v-bind:clearable="false"
                                              label="status"
                                              v-model="statusModel"
                                    ></v-select>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="alert alert-danger"
                                     v-if="statusModel['status_closed']"
                                >
                                    Please note - saving the requirement with this status will 
                                    close the requirement.
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12"
                         v-else
                    >
                        <div class="alert alert-info">
                            Please note - this requirement is closed.
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Requirement Type
                                    <span class="error" v-if="!$v.typeModel.required && $v.typeModel.$dirty"> Please select a type.</span>
                                </label>
                                <v-select :options="typeFixList"
                                          v-bind:disabled="isReadOnly"
                                          v-bind:clearable="false"
                                          label="type"
                                          v-model="typeModel"
                                ></v-select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row"
                 v-if="userLevel > 1"
            >
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

    //VueX
    import { mapGetters } from 'vuex';

    //Validation
    import { required, maxLength } from 'vuelidate/lib/validators';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin.js";
    import loadingModalMixin from "../../mixins/loadingModalMixin.js";

    export default {
        name: "RequirementInformation",
        components: {},
        props: [
            'defaultStakeholderImage',
            'organisationResults',
            'requirementResults',
            'statusList',
            'typeList',
            'userLevel',
        ],
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            }),
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin
        ],
        data() {
            return {
                isReadOnly: false,
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
                    this.showValidationErrorModal();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                this.showLoadingModal('Requirement');

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
                    this.closeLoadingModal();

                    //If the status is closed - refresh the page
                    if (this.statusModel['status_closed']) {
                        window.location.reload();
                    }
                }).catch((error) => {
                    this.showErrorModal(error, this.destination);
                });
            }
        },
        mounted() {
            //Get data from the requirementResults and delegate to the Models
            var requirement_results = this.requirementResults[0]['fields'];

            this.requirementScopeModel = requirement_results['requirement_scope'];
            this.requirementTitleModel = requirement_results['requirement_title'];

            //We need to extract "fields" array from the statusList/typeList json data
            this.statusFixList = this.statusList.map((row) => {
                //Construct the object
                return {
                    'value': row['pk'],
                    'status': row['fields']['requirement_status'],
                    'status_closed': row['fields']['requirement_status_is_closed'],
                };
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

            //Check for the read only
            if (this.statusModel['status_closed'] || this.userLevel === 1) {
                this.isReadOnly = true;
            }
        }
    }
</script>

<style scoped>

</style>
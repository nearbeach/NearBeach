<template>
    <div class="card">
        <div class="card-body">
            <h1>Requirement Item Information</h1>
            <br/>
            <a v-bind:href="`${rootUrl}requirement_information/${requirementItemResults[0]['fields']['requirement']}/`">
                Go Back to requirement
            </a>
            <hr>

            <div class="row">
                <!-- Description -->
                <div class="col-md-4">
                    <h2>Description</h2>
                    <p class="text-instructions">
                        Requirement Items should be detailed. They should only focus on one small section of the
                        requirement.
                    </p>
                </div>

                <!-- Requirement item information -->
                <div class="col-md-8" style="min-height: 610px;">
                    <div class="form-group">
                        <label for="requirement_item_title">
                            Requirement Item Title:
                            <span class="error" v-if="!v$.requirementItemTitleModel.required">
                                Please suppy a title.
                            </span>
                        </label>
                        <input id="requirement_item_title"
                               v-model="requirementItemTitleModel"
                               class="form-control"
                               type="text"
                               required="true"
                               maxlength="255"
                        >
                    </div>
                    <div class="form-group">
                        <label>Requirement Item Scope:
                            <span class="error" v-if="!v$.requirementItemScopeModel.required"> Please supply a scope.</span>
                            <span class="error" v-if="!v$.requirementItemScopeModel.maxLength"> Sorry - too many characters.</span>
                        </label><br/>
                        <img v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
                             class="loader-image"
                             alt="loading image for Tinymce"
                        />
                        <editor
                           :init="{
                             height: 500,
                             menubar: false,
                             plugins: ['lists','table'],
                            toolbar: [
                               'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                               'bold italic strikethrough underline backcolor | table | ' +
                               'bullist numlist outdent indent | removeformat'
                            ]}"
                           v-bind:content_css="false"
                           v-bind:skin="false"
                           v-model="requirementItemScopeModel"
                        />

                    </div>
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
                        <Icon v-bind:icon="icons.linkOut"></Icon> Website:
                        <a v-bind:href="stakeholderModel['organisation_website']" 
                           target="_blank"
                           rel="noopener noreferrer"
                        >
                            {{ stakeholderModel['organisation_website'] }}
                        </a>
                    </div>
                    <div class="organisation-email">
                        <Icon v-bind:icon="icons.mailIcon"></Icon> Email:
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
                            <span class="error" v-if="!v$.statusModel.required && v$.statusModel.$dirty"> Please select a status.</span>
                        </label>
                        <n-select :options="statusFixList"
                                  label="status"
                                  v-model:value="statusModel"
                        ></n-select>
                    </div>

                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label>Requirement Type
                            <span class="error" v-if="!v$.typeModel.required && v$.typeModel.$dirty"> Please select a type.</span>
                        </label>
                        <n-select :options="typeFixList"
                                  label="type"
                                  v-model:value="typeModel"
                        ></n-select>
                    </div>
                </div>
            </div>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateRequirementItem"
                    >Update Requirement</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript Libraries
    import {Modal} from "bootstrap";
    import { Icon } from '@iconify/vue';
    import axios from 'axios';
    import Editor from '@tinymce/tinymce-vue'
    import { NSelect } from 'naive-ui';

    //VueX
    import { mapGetters } from 'vuex';

    //Mixins
    import iconMixin from "../../mixins/iconMixin";

    //Validation
    import useVuelidate from '@vuelidate/core'
    import { required, maxLength } from '@vuelidate/validators'

    export default {
        name: "RequirementItemInformation.vue",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            'editor': Editor,
            Icon,
            NSelect,
        },
        props: {
            requirementItemResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            organisationResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            defaultStakeholderImage: {
                type: String,
                default: "/",
            },
            statusList: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            typeList: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            }),
            getStakeholderImage: function() {
                if (this.stakeholderModel['organisation_profile_picture'] == '') {
                    //There is no image - return the default image
                    return this.defaultStakeholderImage;
                }
                return this.stakeholderModel['organisation_profile_picture']
            },
        },
        mixins: [
            iconMixin,
        ],
        data() {
            return {
                requirementItemScopeModel: '',
                requirementItemTitleModel: '',
                stakeholderModel: '',

                statusFixList: [],
                statusModel: '',
                typeFixList: [],
                typeModel: '',
            };
        },
        validations: {
            requirementItemScopeModel: {
                required,
                maxLength: maxLength(630000),
            },
            requirementItemTitleModel: {
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
            updateRequirementItem: function() {
                // Check the validation first
                this.v$.$touch();

                if (this.v$.$invalid) {
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
                document.getElementById("loadingModalContent").innerHTML = `Updating your Requirement Item details`;

                // Set up the data object to send
                const data_to_send = new FormData();
                data_to_send.set('requirement_item_title', this.requirementItemTitleModel);
                data_to_send.set('requirement_item_scope',this.requirementItemScopeModel);
                data_to_send.set('requirement_item_status',this.statusModel);
                data_to_send.set('requirement_item_type',this.typeModel);

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
                    elem_cont.innerHTML = `<strong>HTML ISSUE:</strong> We could not save the new requirement item<hr>${error}`;

                    // Show the modal
                    var errorModal = new Modal(document.getElementById('errorModal'));
                    errorModal.show();
                });
            }
        },
        mounted() {
            //Get data from the requirementResults and delegate to the Models
            var requirement_item_results = this.requirementItemResults[0]['fields'];

            this.requirementItemScopeModel = requirement_item_results['requirement_item_scope'];
            this.requirementItemTitleModel = requirement_item_results['requirement_item_title'];

            //Extract the organisation results directly
            this.stakeholderModel = this.organisationResults[0]['fields'];

            //Map the original lists to something NSelect can read
            this.statusFixList = this.statusList.map((row) => {
                return {
                    value: row['pk'],
                    label: row['fields']['requirement_item_status'],
                };
            });

            this.typeFixList = this.typeList.map((row) => {
                return {
                    value: row['pk'],
                    label: row['fields']['requirement_item_type'],
                }
            });

            //Set the status and type models
            this.statusModel = requirement_item_results['requirement_item_status'];
            this.typeModel = requirement_item_results['requirement_item_type'];
        },
    }
</script>

<style scoped>

</style>
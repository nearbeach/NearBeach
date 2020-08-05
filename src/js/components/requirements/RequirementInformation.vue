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
                        Place a basic birds eye view of the requirement description here. You will be able to break
                        the requirement down into smaller components called "Items" on the next page.
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
                    <img src="static/NearBeach/images/placeholder/body_text.svg"
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
                <div class="col-md-8">
                    <h3>{{stakeholderModel['organisation_name']}}</h3>
                    <div class="organisation-link">
                        <external-link-icon></external-link-icon> Website:
                        <a v-bind:href="stakeholderModel['organisation_website']" target="_blank">
                            {{ stakeholderModel['organisation_website'] }}
                        </a>
                    </div>
                    <div class="organisation-email">
                        <mail-icon></mail-icon> Email:
                        <a v-bind:href="`mailto:${stakeholderModel['organisation_email']}`">
                            {{stakeholderModel['organisation_email']}}
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript Libraries
    const axios = require('axios');

    //Validation
    import { required, maxLength } from 'vuelidate/lib/validators';

    //Import required Icons
    import { ExternalLinkIcon, MailIcon } from 'vue-feather-icons'

    export default {
        name: "RequirementInformation",
        components: {
            ExternalLinkIcon,
            MailIcon,
        },
        props: [
            'organisationResults',
            'requirementResults',
        ],
        data() {
            return {
                groupModel: '',
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
            groupModel: {
                required,
            },
            requirementScopeModel: {
                required,
                maxLength: maxLength(630000),
            },
            requirementTitleModel: {
                required
            },
            stakeholderModel: {
                required
            },
            statusModel: {
                required
            },
            typeModel: {
                required
            },
        },
        mounted() {
            //Get data from the requirementResults and delegate to the Models
            var requirement_results = this.requirementResults[0]['fields'];

            this.requirementScopeModel = requirement_results['requirement_scope'];
            this.requirementTitleModel = requirement_results['requirement_title'];
            this.statusModel = requirement_results['requirement_status'];
            this.typeModel = requirement_results['requirement_type'];

            //Extract the organisation results directly
            this.stakeholderModel = this.organisationResults[0]['fields'];
        }
    }
</script>

<style scoped>

</style>
<template>
    <div>
        <h2><IconifyIcon v-bind:icon="icons.linkIcon2"></IconifyIcon> Requirement Item Links</h2>
        <p class="text-instructions">
            The following are links for the Items to other projects/tasks.
        </p>

        <!-- ITEM LINKS -->
        <div v-if="itemLinkResults.length === 0"
        >
            <div class="alert alert-dark">
                Sorry - there are no Item Links. Please navigate to the Item you wish to add a link too.
            </div>
        </div>
        <div v-else>
            <table class="table">
                <thead>
                    <tr>
                        <td width="75%">Object Description</td>
                        <td width="25%">Status</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="link in itemLinkResults"
                        :key="link['pk']"
                    >
                        <td v-html="extractObjectDescription(link)"></td>
                        <td>{{extractObjectStatus(link)}}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Submit Button -->
        <!-- TO DO - limit it to certain users -->
        <hr>
        <div class="row submit-row">
            <div class="col-md-12">
                <a href="javascript:void(0)"
                   class="btn btn-primary save-changes"
                   v-on:click="newRequirementItemLink"
                >Create new Link</a>
            </div>
        </div>


        <!-- LINKING MODAL -->
        <!-- need to build something that resets the requirement links when adding links -->
        <new-requirement-link-wizard v-bind:location-id="locationId"
                                     v-bind:destination="destination"
                                     v-on:update_module="updateModel($event)"
        ></new-requirement-link-wizard>
    </div>
</template>

<script>
    const axios = require('axios');
    import {Modal} from "bootstrap";

    //VueX
    import { mapGetters } from 'vuex';

    //Mixins
    import iconMixin from "../../../mixins/iconMixin";

    export default {
        name: "RequirementItemLinksModule",
        props: {
            destination: {
                type: String,
                default: '',
            },
            locationId: {
                type: Number,
                default: 0,
            },
        },
        mixins: [
            iconMixin,
        ],
        data() {
            return {
                itemLinkResults: [],
            }
        },
        computed: {
            ...mapGetters({
                rootUrl: 'getRootUrl',
            })
        },
        methods: {
            extractObjectDescription: function(link) {
                /*
                The following function will accept a link in. It will then check what that link is connected to. From
                there it will determine which fields it will extract out.
                 */
                var object_description = 'ERROR',
                    object_id = 'ERROR',
                    object_link = '/',
                    requirement_item_description = '';

                if (link['opportunity_id'] !== null) {
                    object_description = link['opportunity_id__opportunity_name'];
                    object_id = `Opportunity ${link['opportunity_id']}`;
                    object_link = `${this.rootUrl}opportunity_information/${link['opportunity_id']}`;
                } else if (link['project_id'] !== null) {
                    object_description = link['project_id__project_name'];
                    object_id = `Project ${link['project_id']}`;
                    object_link = `${this.rootUrl}project_information/${link['project_id']}`;
                } else if (link['quote_id'] !== null) {
                    object_description = link['quote_id__quote_title'];
                    object_id = `Quote ${link['quote_id']}`;
                    object_link = `${this.rootUrl}quote_information/${link['quote_id']}`;
                } else if (link['task_id'] !== null) {
                    object_description = link['task_id__task_short_description'];
                    object_id = `Task ${link['task_id']}`;
                    object_link = `${this.rootUrl}task_information/${link['task_id']}`;
                }

                //Check to see if we need to inser the requirement item description.
                if (link['requirement_id'] !== null) {
                    requirement_item_description = `<p class="requirement-item-link-type">${link['requirement_item_id__requirement_item_title']}</p>`;
                    object_id = `${object_id} / Item ${link['requirement_id']}`;
                }

                //Return the HTML
                return `
                    <a href="${object_link}">
                        <p>
                            ${object_description}
                        </p>
                        <div class="spacer"></div>
                        ${requirement_item_description}
                        <p class="requirement-link-type">
                            ${object_id}
                        </p>
                    </a>
                `;
            },
            extractObjectStatus: function(link) {
                /*
                The following function will accept a link in. It will then check what that link is connected to. From
                there it will determine what status field it will extract out.
                 */
                var object_status = 'ERROR';

                if (link['opportunity_id'] !== null) {
                    object_status = link['opportunity_id__opportunity_stage_id__opportunity_stage_description'];
                } else if (link['project_id'] !== null) {
                    object_status = link['project_id__project_status'];
                } else if (link['quote_id'] !== null) {
                    object_status = link['quote_id__quote_title'];
                } else if (link['task_id'] !== null) {
                    object_status = link['task_id__task_status'];
                }

                return object_status;

            },
            updateLinkResults: function() {
                //Get the data from the database
                axios.post(
                    'data/links/',
                ).then((response) => {
                    this.itemLinkResults = response['data'];
                });
            },
            newRequirementItemLink: function() {
                //Open up the modal
                var elem_modal = new Modal(document.getElementById('newRequirementLinkModal'));
                elem_modal.show();
            },
            updateModel: function(data) {
                this.itemLinkResults = data;
            },
        },
        mounted() {
            //Get the required data we need
            this.updateLinkResults();
        },
    }
</script>

<style scoped>

</style>

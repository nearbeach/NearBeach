<template>
    <div>
        <h2><IconifyIcon v-bind:icon="icons.linkIcon"></IconifyIcon> Requirement Links</h2>
        <p class="text-instructions">
            The following are links to other projects/tasks. You can link a Requirement to these other objects to
            symbolise a connection between the two.
        </p>

        <!-- REQUIREMENT LINKS -->
        <div v-if="linkResults.length === 0"
             class="requirement-item-spacer"
        >
            <div class="alert alert-dark">Sorry - there are no Links for this requirement.</div>
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
                    <tr v-for="link in linkResults">
                        <td v-html="extractObjectDescription(link)"></td>
                        <td>
                            {{extractObjectStatus(link)}}
                            <span class="remove-link">
                                <IconifyIcon v-bind:icon="icons.trashCan"
                                             v-on:click="removeLink(link.object_assignment_id)"
                                />
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Submit Button -->
        <!-- TO DO - limit it to certain users -->
        <div class="row submit-row">
            <div class="col-md-12">
                <a href="javascript:void(0)"
                   class="btn btn-primary save-changes"
                   v-on:click="newRequirementLink"
                >Create new Link</a>
            </div>
        </div>
        <hr>

        <h2><IconifyIcon v-bind:icon="icons.linkIcon2"></IconifyIcon> Requirement Item Links</h2>
        <p class="text-instructions">
            The following are links for the Items to other projects/tasks.
        </p>

        <!-- ITEM LINKS -->
        <div v-if="itemLinkResults.length == 0"
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
                    <tr v-for="link in itemLinkResults">
                        <td v-html="extractObjectDescription(link)"></td>
                        <td>{{extractObjectStatus(link)}}</td>
                    </tr>
                </tbody>
            </table>
        </div>


        <!-- LINKING MODAL -->
        <!-- need to build something that resets the requirement links when adding links -->
        <new-requirement-link-wizard v-bind:location-id="locationId"
                                     v-bind:destination="'requirement'"
                                     v-on:update_module="updateModel"
        ></new-requirement-link-wizard>


    </div>
</template>

<script>
    //JavaScript components
    import {Modal} from "bootstrap";
    const axios = require('axios');

    //VueX
    import { mapGetters } from 'vuex';

    //Mixins
    import iconMixin from "../../../mixins/iconMixin";

    export default {
        name: "RequirementLinksModule",
        props: [
            'activateLazyLoading',
            'destination',
            'locationId',
        ],
        mixins: [
            iconMixin,
        ],
        data() {
            return {
                linkResults: [],
                itemLinkResults: [],
                linkModel: [],
            };
        },
        computed: {
            ...mapGetters({
                rootUrl: 'getRootUrl',
            }),
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

                if (link['project_id'] !== null) {
                    object_description = link['project_id__project_name'];
                    object_id = `Project ${link['project_id']}`;
                    object_link = `/project_information/${link['project_id']}`;
                } else if (link['task_id'] !== null) {
                    object_description = link['task_id__task_short_description'];
                    object_id = `Task ${link['task_id']}`;
                    object_link = `/task_information/${link['task_id']}`;
                }

                //Check to see if we need to insert the requirement item description.
                if (link['requirement_item_id'] !== null) {
                    requirement_item_description = `<p class="requirement-item-link-type">${link['requirement_item_id__requirement_item_title']}</p>`;
                    object_id = `${object_id} / Item ${link['requirement_item_id']}`;
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

                if (link['project_id'] !== null) {
                    object_status = link['project_id__project_status'];
                } else if (link['task_id'] !== null) {
                    object_status = link['task_id__task_status'];
                }

                return object_status;

            },
            newRequirementLink: function() {
                //Open up the modal
                var elem_modal = new Modal(document.getElementById('newRequirementLinkModal'));
                elem_modal.show();
            },
            removeLink: function(link_id) {
                //Use Axios to send data to the backend
                const data_to_send = new FormData();
                data_to_send.set('object_assignment_id', link_id);

                //Tell the backend to remove the data.
                axios.post(
                    `${this.rootUrl}object_data/delete_link/`,
                    data_to_send,
                ).then(response => {
                    //Remove the old link_id from the linkResults
                    this.linkResults = this.linkResults.filter(row => {
                        return row.object_assignment_id !== link_id;
                    });
                })
            },
            updateItemLinkResults: function() {
                //Get the data from the database
                axios.post(
                    'data/item_links/',
                ).then((response) => {
                    this.itemLinkResults = response['data'];
                });
            },
            updateLinkResults: function() {
                //Get the data from the database
                axios.post(
                    'data/links/',
                ).then((response) => {
                    this.linkResults = response['data'];
                });
            },
            updateModel: function() {
                this.updateLinkResults();
                this.updateItemLinkResults();
            },
        },
        mounted() {
            this.updateModel();
        },
    }
</script>

<style scoped>

</style>

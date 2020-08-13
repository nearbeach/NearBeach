<template>
    <div>
        <h2><i data-feather="link"></i> Requirement Links</h2>
        <p class="text-instructions">
            The following are links to other projects/tasks. You can link a Requirement to these other objects to
            symbolise a connection between the two.
        </p>

        <!-- REQUIREMENT LINKS -->
        <div v-if="linkResults.length == 0"
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
                >Create new Link</a>
            </div>
        </div>

        <h2><i data-feather="link-2"></i> Requirement Item Links</h2>
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

    </div>
</template>

<script>
    //JavaScript components
    const axios = require('axios');

    export default {
        name: "RequirementLinksModule",
        props: [
            'activateLazyLoading',
        ],
        data() {
            return {
                linkResults: [],
                itemLinkResults: [],
            };
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

                if (link['opportunity_id'] != null) {
                    object_description = link['opportunity_id__opportunity_name'];
                    object_id = `Opportunity ${link['opportunity_id']}`;
                    object_link = `/opportunity_information/${link['opportunity_id']}`;
                } else if (link['project_id'] != null) {
                    object_description = link['project_id__project_name'];
                    object_id = `Project ${link['project_id']}`;
                    object_link = `/project_information/${link['project_id']}`;
                } else if (link['quote_id'] != null) {
                    object_description = link['quote_id__quote_title'];
                    object_id = `Quote ${link['quote_id']}`;
                    object_link = `/quote_information/${link['quote_id']}`;
                } else if (link['task_id'] != null) {
                    object_description = link['task_id__task_short_description'];
                    object_id = `Task ${link['task_id']}`;
                    object_link = `/task_information/${link['task_id']}`;
                }

                //Check to see if we need to inser the requirement item description.
                if (link['requirement_id'] != null) {
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

                if (link['opportunity_id'] != null) {
                    object_status = link['opportunity_id__opportunity_stage_id__opportunity_stage_description'];
                } else if (link['project_id'] != null) {
                    object_status = link['project_id__project_status'];
                } else if (link['quote_id'] != null) {
                    object_status = link['quote_id__quote_title'];
                } else if (link['task_id'] != null) {
                    object_status = link['task_id__task_status'];
                }

                return object_status;

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
        },
        mounted() {
            this.updateLinkResults();
            this.updateItemLinkResults();
        },
    }
</script>

<style scoped>

</style>
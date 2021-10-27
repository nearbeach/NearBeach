<template>
    <div>
        <h2><IconifyIcon v-bind:icon="icons.linkOut"></IconifyIcon> {{destination}} Links</h2>
        <p class="text-instructions">
            The following are links to other objects like projects/tasks/requirements. You can link a {{destination}}
            to these other objects to symbolise a connection between the two.
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
                    <tr v-for="(link, i) in linkResults">
                        <td>
                            <a :href="objectDescriptions[i].link_location + objectDescriptions[i].link_id">
                                <p>{{objectDescriptions[i].link_title}}</p>
                                <div class="spacer"></div>
                                <p class="small-text">{{objectDescriptions[i].link_text}}</p>
                            </a>
                        </td>
                        <td>{{extractObjectStatus(link)}}</td>
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
                   v-on:click="newLink"
                >Create new Link</a>
            </div>
        </div>
        <hr>

        <!-- MODAL FOR NEW OBJECT LINKS -->
        <new-link-wizard v-bind:destination="destination"
                         v-bind:location-id="locationId"
                         v-on:update_link_results="updateLinkResults"
        ></new-link-wizard>
    </div>
</template>

<script>
    import { Modal } from "bootstrap";

    const axios = require('axios');

    //Mixins
    import iconMixin from "../../../mixins/iconMixin";

    export default {
        name: "ObjectLinks",
        props: {
            destination: String,
            locationId: Number,
        },
        mixins: [
            iconMixin,
        ],
        data() {
            return {
                linkResults: [],
            }
        },
        computed: {
            objectDescriptions() {
                return this.linkResults.map(this.extractObjectDescription);
            }
        },
        methods: {
            extractObjectDescription: function(link) {
                //Declare some variables
                var link_title = '',
                    link_id = '',
                    link_text = '',
                    link_location = '';

                if (link['project_id'] !== null && this.destination !== 'project') {
                    // The link is a project link
                    link_title = link['project_id__project_name'];
                    link_id = link['project_id'];
                    link_text = `Project ${link['project_id']}`;
                    link_location = '/project_information/';
                } else if (link['requirement_id'] !== null) {
                    // The link is a requirement link
                    link_title = link['requirement_id__requirement_title'];
                    link_id = link['requirement_id'];
                    link_text = `Requirement ${link['requirement_id']}`;
                    link_location = '/requirement_information/';
                } else if (link['requirement_item_id'] !== null) {
                    // The link is a requirement item link
                    link_title = link['requirement_item_id__requirement_item_title'];
                    link_id = link['requirement_item_id'];
                    link_text = `Requirement Item ${link['requirement_item_id']}`;
                    link_location = '/requirement_item_information/';
                } else if (link['task_id'] !== null && this.destination !== 'task') {
                    // The link is a requirement item link
                    link_title = link['task_id__task_short_description'];
                    link_id = link['task_id'];
                    link_text = `Task ${link['task_id']}`;
                    link_location = '/task_information/';
                }

                return { link_title, link_id, link_text, link_location };
            },
            extractObjectStatus: function(link) {
                //Declare some variables
                var link_status = '';

                if (link['project_id'] !== null && this.destination !== 'project') {
                    // The link is a project link
                    link_status = link['project_id__project_status'];
                } else if (link['requirement_id'] !== null) {
                    // The link is a requirement link
                    link_status = link['requirement_id__requirement_status__requirement_status'];
                } else if (link['requirement_item_id'] !== null) {
                    // The link is a requirement item link
                    link_status = link['requirement_item_id__requirement_item_status__requirement_item_status'];
                } else if (link['task_id'] !== null && this.destination !== 'task') {
                    // The link is a requirement item link
                    link_status = link['task_id__task_status'];
                }

                return `${link_status}`;
            },
            newLink: function() {
                //Open up the modal
                
                var elem_modal = new Modal(document.getElementById('newLinkModal'));
                
                elem_modal.show();
                
            },
            updateLinkResults: function() {
                //Get the data from the database
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/object_link_list/`,
                ).then((response) => {
                    this.linkResults = response['data'].filter(row => {
                        /*
                        We want to filter out any rows where the only link available is just the destination/locationID's
                        link. For example, this object row might be linked to a customer - and that data is not shown
                        here.

                        Method
                        ~~~~~~
                        Add all the unique id's together. If the sum of these numbers equals the location id, it means
                        that the only data in this is the destination/locationID. We want to filter out these values.
                         */

                        var sum = parseInt(0 + row['project_id']) + parseInt(0 + row['requirement_id']) +
                            parseInt(0 + row['requirement_item_id']) + parseInt(0 + row['task_id']);

                        return sum > this.locationId;
                    });
                });
            },
        },
        mounted() {
            //Get data
            this.updateLinkResults();
        },
    }
</script>

<style scoped>

</style>
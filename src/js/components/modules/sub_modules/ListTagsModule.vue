<template>
    <div>
        <h2>Assigned Tags</h2>
        <p class="text-instructions">
            Here are all tags associated with this {{destination}}. You can add more
            tags by clicking on the "Add Tag" button.
        </p>
        <div class="tag-list">
            <div v-for="tag in tagList"
                 :key="tag['pk']"
                 class="single-tag"
                 v-bind:style="`background-color: #${tag['fields']['tag_colour']};`"
            >
                {{tag['fields']['tag_name']}}
                <span v-on:click="removeTag(tag['pk'])"
                >
                    <IconifyIcon v-bind:icon="icons.xCircle"></IconifyIcon>
                </span>
            </div>
        </div>

        <!-- ADD TAG BUTTON -->
        <hr>
        <div class="row submit-row">
            <div class="col-md-12">
                <a href="javascript:void(0)"
                   class="btn btn-primary save-changes"
                   v-on:click="createNewTag"
                >Add Tag to {{destination}}</a>
            </div>
        </div>

        <!-- ADD TAG MODULE -->
        <add-tag-wizard v-bind:destination="destination"
                        v-bind:location-id="locationId"
                        v-bind:assigned-tags="tagList"
                        v-on:add_tags="addTags($event)"
        ></add-tag-wizard>

    </div>
</template>

<script>
    const axios = require('axios');
    import {Modal} from "bootstrap";
    
    //Mixin
    import iconMixin from "../../../mixins/iconMixin";
    import AddTagWizard from '../wizards/AddTagWizard.vue';

    export default {
        components: { AddTagWizard },
        name: "ListTagsModule",
        props: {
            destination: String,
            locationId: Number,
        },
        data() {
            return {
                tagList: [],
            }
        },
        mixins: [
            iconMixin,
        ],
        methods: {
            addTags: function(data) {
                this.tagList = data;
            },
            createNewTag: function() {
                //Open up modal
                var newTagModal = new Modal(document.getElementById('addTagModal'));
                newTagModal.show();
            },
            getAssignedTags: function() {
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/tag_list/`
                ).then(response => {
                    this.tagList = response['data'];
                }).catch(error => {
                    console.log("ERROR WITH DATA: ",error);
                })
            },
            removeTag: function(tag_id) {
                //Create data_to_send
                const data_to_send = new FormData();
                data_to_send.set('tag', tag_id);
                data_to_send.set('object_enum', this.destination);
                data_to_send.set('object_id', this.locationId);

                //Send data using axios
                axios.post(
                    `/object_data/delete_tag/`,
                    data_to_send,
                ).then(response => {
                    //Remove data from tagList
                    this.tagList = this.tagList.filter(row => {
                        return row['pk'] !== tag_id;
                    });
                }).catch(error => {
                    console.log("ERROR: ",error);
                });
            },
        },
        mounted() {
            this.getAssignedTags();
        }
    }
</script>

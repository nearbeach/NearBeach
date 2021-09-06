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
    </div>
</template>

<script>
    const axios = require('axios');
    
    //Mixin
    import iconMixin from "../../../mixins/iconMixin";

    export default {
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

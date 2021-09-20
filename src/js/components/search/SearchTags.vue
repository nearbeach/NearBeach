<template xmlns:v-bind="http://www.w3.org/1999/xhtml">
    <div class="card">
        <div class="card-body">
            <h1>Search Tags</h1>
            <hr>
            
            <div class="row">
                <div class="col-md-4">
                    <strong>Tags</strong>
                    <p class="text-instructions">
                        Use the search bar to help you find any tags.
                    </p>

                    <p class="text-instructions">
                        Click on the icon <IconifyIcon v-bind:icon="icons.infoCircle"></IconifyIcon>
                        to edit the tag.
                    </p>

                    <p class="text-instructions">
                        To add in any new tags - please click on the "New Tag" button.
                    </p>
                </div>

                <div class="col-md-8 tag-list">
                    <div v-for="tag in localTagResults"
                         v-bind:key="tag['pk']" 
                         v-bind:style="`background-color: ${tag['fields']['tag_colour']};`"
                         v-on:dblclick="editTag(tag['pk'])"
                         class="single-tag"
                    >
                        {{tag['fields']['tag_name']}}
                        <span v-on:click="editTag(tag['pk'])"
                        >
                            <IconifyIcon v-bind:icon="icons.infoCircle"></IconifyIcon>
                        </span>
                    </div>
                </div>

                <!-- ADD NEW TAG BUTTON -->
                <hr>
                <div class="row submit-row">
                    <div class="col-md-12">
                        <a href="javascript:void(0)"
                           class="btn btn-primary save-changes"
                           v-on:click="addTag"
                        >Add Tag</a>
                    </div>
                </div>
            </div>

            <!-- MODALS -->
            <edit-tag-modal v-bind:single-tag="singleTag"
                            v-on:new_tag="newTag"
                            v-on:update_tags="updateTags"
            ></edit-tag-modal>
        </div>
    </div>
</template>

<script>
    //MIXINS
    import iconMixin from '../../mixins/iconMixin';
    import { Modal } from 'bootstrap';

    export default {
        name: 'SearchTags',
        props: {
            tagResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        data() {
            return {
                singleTag: {
                    tagName: '',
                    tagColour: '',
                },
                localTagResults: this.tagResults,
            }
        },
        mixins: [
            iconMixin
        ],
        methods: {
            addTag: function() {
                //Send data down to the modal
                this.singleTag['tagName'] = 'default tag';
                this.singleTag['tagId'] = 0;
                this.singleTag['tagColour'] = '#37cbd2';

                //Open up modal
                let edit_tag_modal = new Modal(document.getElementById('editTagModal'));
                edit_tag_modal.show();
            },
            editTag: function(tag_id) {
                //Filter for the tag information
                let single_tag = this.localTagResults.filter(row => {
                    return row['pk'] == tag_id;
                })[0];

                //Send data down to the modal
                this.singleTag['tagName'] = single_tag['fields']['tag_name'];
                this.singleTag['tagId'] = tag_id;
                this.singleTag['tagColour'] = single_tag['fields']['tag_colour'];

                //Open up modal
                let edit_tag_modal = new Modal(document.getElementById('editTagModal'));
                edit_tag_modal.show();
            },
            newTag: function(data) {
                console.log("Data: ",data);
                this.localTagResults.push(data[0]);
            },
            updateTags: function(data) {
                //Get the index location of the object we are updating
                let index = this.localTagResults.findIndex( row => {
                    return row['pk'] === data['tag_id'];
                });

                // Update the data
                this.localTagResults[index]['fields']['tag_name'] = data['tag_name'];
                this.localTagResults[index]['fields']['tag_colour'] = data['tag_colour'];
            }
        }
    }
</script>

<template>
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
                    <div v-for="tag in tagResults" 
                         v-bind:key="tag['pk']" 
                         v-bind:style="`background-color: #${tag['fields']['tag_colour']};`"
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
            <edit-tag-modal v-bind:single-tag="singleTag"></edit-tag-modal>
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
            }
        },
        mixins: [
            iconMixin
        ],
        methods: {
            addTag: function() {
                //ADD CODE
            },
            editTag: function(tag_id) {
                //Filter for the tag information
                let single_tag = this.tagResults.filter(row => {
                    return row['pk'] == tag_id;
                })[0];

                //Send data down to the modal
                this.singleTag['tagName'] = single_tag['fields']['tag_name'];
                this.singleTag['tagColour'] = single_tag['fields']['tag_colour'];

                //Open up modal
                let edit_tag_modal = new Modal(document.getElementById('editTagModal'));
                edit_tag_modal.show();
            }
        }
    }
</script>

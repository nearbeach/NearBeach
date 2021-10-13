<template>
    <div class="modal fade" id="addTagModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><IconifyIcon v-bind:icon="icons.usersIcon"></IconifyIcon> Add Tags Wizard</h2>
                    <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            id="addTagsCloseButton"
                    >
                        <span aria-hidden="true"></span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Add Tag</strong>
                            <p class="text-instructions">
                                Use the dropdown to select one or many lables to add to the {{destination}}.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <label>All Tag List</label>
                            <v-select label="tag" 
                                      multiple
                                      :options="tagList"
                                      v-model="tagModel"
                            ></v-select>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                    >Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-on:click="addTag"
                    >Add Tag</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript extras
    import errorModalMixin from "../../../mixins/errorModalMixin";
    import iconMixin from "../../../mixins/iconMixin";

    const axios = require('axios');

    export default {
        name: "AddTagWizard",
        props: {
            assignedTags: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            destination: String,
            locationId: Number,
        },
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        data() {
            return {
                allTagList: [],
                tagModel: [],
            }
        },
        computed: {
            tagList: function() {
                return this.allTagList.filter(row => {
                    return this.assignedTags.findIndex(tag => {
                        return tag['pk'] == row['value'];
                    }) < 0;
                });
            }
        },
        methods: {
            addTag: function() {
                //Construct data_to_send
                const data_to_send = new FormData();

                //Loop through all the models results
                this.tagModel.forEach(row => {
                    data_to_send.append('tag_id', row['value']);
                });

                //Use Axios to send data to backend
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/add_tags/`,
                    data_to_send
                ).then(response => {
                    //Emit data up
                    this.$emit('add_tags',response['data']);

                    //Close the modal
                    document.getElementById('addTagsCloseButton').click();

                    //Clear the results
                    this.tagModel = [];
                })
            },
            getTagList: function() {
                axios.post(
                    `/object_data/tag_list_all/`
                ).then(response => {
                    //Map data to the preferred data format for vue-select
                    this.allTagList = response['data'].map(row => {
                        return {
                            value: row['pk'],
                            tag: row['fields']['tag_name'],
                        }
                    });
                }).catch(error => {
                    
                })
            },
        },
        mounted() {
            //Get the tag list
            this.getTagList();
        }
    }
</script>

<style scoped>

</style>

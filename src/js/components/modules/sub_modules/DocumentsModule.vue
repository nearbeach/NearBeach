<template>
    <div>
        <h2><i data-feather="briefcase"></i> Documents</h2>
        <p class="text-instructions">
            The following is a folder structure of all documents uploaded to this {{destination}}
        </p>

        <!-- DOCUMENT FOLDER TREE -->
        <div v-if="documentFilteredList.length + folderFilteredList.length == 0"
             class="module-spacer"
        >
            <div class="alert alert-dark">Sorry - there are no documents or folders uploaded.</div>
        </div>
        <div v-else class="document-widget">
            <!-- GO TO PARENT DIRECTORY -->
            <div v-if="this.currentFolder != null"
                 class="document-child"
            >
                <i data-feather="arrow-up" width="80px" height="80px" stroke-width="1"></i>
                <p class="text-instructions">
                    Go to Parent Directory...
                </p>
            </div>

            <!-- RENDER THE FOLDERS -->
            <div v-for="folder in folderFilteredList" class="document-child">
                <i data-feather="folder" width="80px" height="80px" stroke-width="1"></i>
                <p class="text-instructions">
                    {{shortName(folder['fields']['folder_description'])}}
                </p>
            </div>

            <!-- RENDER THE FILES -->
            <div v-for="document in documentList" class="document-child">
                <i v-bind:data-feather="getIcon(document)"
                   width="80px"
                   height="80px"
                   stroke-width="1"
                ></i>
                <p class="text-instructions">
                    {{shortName(document['document_key__document_description'])}}
                </p>
            </div>
            <!--
            <div v-for="item in documentList" class="document-child">
                <i data-feather="image" width="80px" height="80px" stroke-width="1"></i>
                <p class="text-instructions">
                    {{shortName("The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog")}}
                </p>
            </div>
            <div v-for="item in documentList" class="document-child">
                <i data-feather="external-link" width="80px" height="80px" stroke-width="1"></i>
                <p class="text-instructions">
                    {{shortName("The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog")}}
                </p>
            </div>
            -->
        </div>

        <!-- ADD DOCUMENTS AND FOLDER BUTTON -->
        <hr>
        <div class="btn-group save-changes">
            <button class="btn btn-primary dropdown-toggle"
                    type="button"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false"
            >
                New Document/File
            </button>
            <div class="dropdown-menu">
                <a class="dropdown-item" href="javascript:void(0)">New File Upload</a>
                <a class="dropdown-item" href="javascript:void(0)">New File URL Link</a>
                <!--<a class="dropdown-item" href="javascript:void(0)">New Whiteboard</a>-->
                <a class="dropdown-item" href="javascript:void(0)">New Folder</a>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    const feather = require('feather-icons')

    export default {
        name: "DocumentsModule",
        props: [
            'destination',
            'locationId',
        ],
        data() {
            return {
                currentFolder: null,
                documentList: [],
                documentFilteredList: [],
                folderList: [],
                folderFilteredList: [],
            }
        },
        methods: {
            getDocumentList: function() {
                axios.post(
                    `/documentation/${this.destination}/${this.locationId}/list/files/`,
                ).then(response => {
                    this.documentList = response['data'];

                    this.updateDocumentFilteredList();
                });
            },
            getFolderList: function() {
                axios.post(
                    `/documentation/${this.destination}/${this.locationId}/list/folders/`,
                ).then(response => {
                    this.folderList = response['data'];

                    this.updateFolderFilteredList();
                });
            },
            getIcon: function(document) {
                //If the document is a weblink - just return the link image
                if (document['document_key__document_url_location'] != "") {
                    return 'external-link';
                }

                //We know the document is not a link - now we use the suffix to the document name to determine the icon
                var split_document = document['document_key__document'].split(".");

                //Get the last result
                var document_suffic = split_document[split_document.length - 1];

                switch(document_suffic) {
                    case 'jpg':
                    case 'png':
                    case 'bmp':
                      return 'image';
                    default:
                      return 'file-text';
                }
            },
            shortName: function(input_string) {
                //The following method will determine if we need an ellipsis (...) at the end of the file/folder name
                const max_string_length = 50;

                //If string is less than the max length, then just return the string
                if (input_string.length <= max_string_length) {
                    return input_string;
                }

                //Now we split the string by max_string_length - 3 (3 for the ...)
                var new_string = `${input_string.substring(0,max_string_length-3)}...`;

                //Return the new string
                return new_string;
            },
            updateDocumentFilteredList: function() {
                //Filter the results to contain only the documents in the current folder
                this.documentFilteredList = this.documentList.filter(row => {
                    return row['folder'] == this.currentFolder;
                });
            },
            updateFolderFilteredList: function() {
                //Filter the results to contain only the folders in the current folder
                this.folderFilteredList = this.folderList.filter(row => {
                    return row['fields']['parent_folder'] == this.currentFolder;
                })
            }
        },
        mounted() {
            this.getDocumentList();
            this.getFolderList();
        },
        updated() {
            feather.replace();
        }
    }
</script>

<style scoped>

</style>
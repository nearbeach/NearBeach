<template>
    <div>
        <h2><IconifyIcon :icon="icons.bxBriefcase" /> Documents</h2>
        <p class="text-instructions">
            The following is a folder structure of all documents uploaded to this {{destination}}
        </p>

        <!-- DOCUMENT FOLDER TREE -->
        <div v-if="documentList.length + folderList.length == 0"
             class="module-spacer"
        >
            <div class="alert alert-dark">Sorry - there are no documents or folders uploaded.</div>
        </div>
        <div v-else class="document-widget">
            <!-- GO TO PARENT DIRECTORY -->
            <div v-if="this.currentFolder != null"
                 v-on:click="goToParentDirectory()"
                 class="document-child"
            >
                <IconifyIcon v-bind:icon="icons.arrowUp"
                             width="80px"
                             height="80px"
                />
                <p class="text-instructions">
                    Go to Parent Directory...
                </p>
            </div>

            <!-- RENDER THE FOLDERS -->
            <div v-for="folder in folderFilteredList"
                 :key="folder.pk"
                 v-on:click="updateCurrentFolder(folder['pk'])"
                 class="document-child"
            >
                <IconifyIcon v-bind:icon="icons.folderIcon"
                             width="80px"
                             height="80px"
                />
                <p class="text-instructions">
                    {{shortName(folder['fields']['folder_description'])}}
                </p>
            </div>

            <!-- RENDER THE FILES -->
            <div v-for="document in documentFilteredList" 
                 :key="document.document_key_id"
                 class="document-child"
            >
                <a v-bind:href="`/private/${document['document_key_id']}/`" 
                   rel="noopener noreferrer"
                   target="_blank"
                >
                    <IconifyIcon v-bind:icon="getIcon(document)"
                                 width="80px"
                                 height="80px"
                    />
                    <p class="text-instructions">
                        {{shortName(document['document_key__document_description'])}}
                    </p>
                </a>
            </div>
        </div>

        <!-- ADD DOCUMENTS AND FOLDER BUTTON -->
        <hr>
        <div class="btn-group save-changes">
            <button class="btn btn-primary dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
            >
                New Document/File
            </button>
            <ul class="dropdown-menu">
                <li>
                    <a class="dropdown-item"
                       href="javascript:void(0)"
                       v-on:click="uploadDocument"
                    >
                        Upload Document
                    </a>
                </li>
                <li>
                    <a class="dropdown-item"
                       href="javascript:void(0)"
                       v-on:click="addLink"
                    >
                        Add Link
                    </a>
                </li>
                <li>
                    <a class="dropdown-item"
                       href="javascript:void(0)"
                       v-on:click="addFolder"
                    >
                        Add Folder
                    </a>
                </li>
            </ul>
        </div>

        <!-- MODALS -->
        <!-- ADD FOLDER ID -->
        <add-folder-wizard v-bind:destination="destination"
                           v-bind:location-id="locationId"
                           v-bind:current-folder="currentFolder"
                           v-bind:existing-folders="folderFilteredList"
                           v-on:update_folder_list="updateFolderList($event)"
        ></add-folder-wizard>

        <!-- ADD LINK WIZARD -->
        <add-link-wizard v-bind:destination="destination"
                         v-bind:location-id="locationId"
                         v-bind:current-folder="currentFolder"
                         v-bind:exclude-documents="documentFilteredList"
                         v-on:update_document_list="updateDocumentList($event)"
        ></add-link-wizard>

        <!-- UPLOAD DOCUMENT WIZARD -->
        <upload-document-wizard v-bind:destination="destination"
                                v-bind:location-id="locationId"
                                v-bind:current-folder="currentFolder"
                                v-bind:exclude-documents="documentFilteredList"
                                v-on:update_document_list="updateDocumentList($event)"
        ></upload-document-wizard>
    </div>
</template>

<script>
    const axios = require('axios');
    import {Modal} from "bootstrap";

    //Mixins
    import iconMixin from "../../../mixins/iconMixin";

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
        mixins: [
            iconMixin,
        ],
        methods: {
            addFolder: function() {
                var addFolderModal = new Modal(document.getElementById('addFolderModal'));
                addFolderModal.show();

            },
            addLink: function() {
                var addLinkModal = new Modal(document.getElementById("addLinkModal"));
                addLinkModal.show();
            },
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
                if (document['document_key__document_url_location'] != "" &&
                    document['document_key__document_url_location'] !== null) {
                    return this.icons.linkOut;
                }

                //We know the document is not a link - now we use the suffix to the document name to determine the icon
                var split_document = document['document_key__document'].split(".");

                //Get the last result
                var document_suffic = split_document[split_document.length - 1];

                switch(document_suffic) {
                    case 'jpg':
                    case 'png':
                    case 'bmp':
                      return this.icons.imageIcon;
                    case 'doc':
                    case 'docx':
                        return this.icons.microsoftWord;
                    case 'xls':
                    case 'xlsx':
                        return this.icons.microsoftExcel;
                    case 'ppt':
                    case 'pptx':
                        return this.icons.microsoftPowerpoint;
                    case 'pdf':
                        return this.icons.documentPdf;
                    default:
                      return this.icons.documentText;
                }
            },
            goToParentDirectory: function() {
                //Filter for the directory - then obtain it's parent directory variable.
                var filtered_data = this.folderList.filter(row => {
                    return row['pk'] == this.currentFolder;
                })[0];

                //Update the current directory to the parent folder
                this.updateCurrentFolder(filtered_data['fields']['parent_folder']);
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
            updateCurrentFolder: function(new_folder_id) {
                //Update the current folder id
                this.currentFolder = new_folder_id;

                //Update the filtered lists
                this.updateDocumentFilteredList();
                this.updateFolderFilteredList();
            },
            updateDocumentList: function(data) {
                //Add data to the docuemnt List
                this.documentList.push(data[0]);

                //Update the filtered list
                this.updateDocumentFilteredList();
            },
            updateDocumentFilteredList: function() {
                //Filter the results to contain only the documents in the current folder
                this.documentFilteredList = this.documentList.filter(row => {
                    return row['folder'] == this.currentFolder;
                });
            },
            updateFolderList: function(data) {
                //Append the first row of the data (there will always be one row)
                this.folderList.push(data[0]);

                //Update the folder filtered list
                this.updateFolderFilteredList();
            },
            updateFolderFilteredList: function() {
                //Filter the results to contain only the folders in the current folder
                this.folderFilteredList = this.folderList.filter(row => {
                    return row['fields']['parent_folder'] == this.currentFolder;
                })
            },
            uploadDocument: function() {
                var uploadDocumentModal = new Modal(document.getElementById('uploadDocumentModal'));
                uploadDocumentModal.show();
            },
        },
        mounted() {
            this.getDocumentList();
            this.getFolderList();
        },
    }
</script>

<style scoped>

</style>
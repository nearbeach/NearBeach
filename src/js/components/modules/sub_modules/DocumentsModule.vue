<template>
    <div>
        <h2><i data-feather="briefcase"></i>Documents</h2>
        <p class="text-instructions">
            The following is a folder structure of all documents uploaded to this {{destination}}
        </p>

        <!-- DOCUMENT FOLDER TREE -->
        <div v-if="documentList.length == 0"
             class="module-spacer"
        >
            <div class="alert alert-dark">Sorry - there are no documents or folders uploaded.</div>
        </div>
        <div v-else class="document-widget">
            <!-- GO TO PARENT DIRECTORY -->
            <div class="document-child">
                <i data-feather="arrow-up" width="80px" height="80px" stroke-width="1"></i>
                <p class="text-instructions">
                    Go to Parent Directory...
                </p>
            </div>

            <!-- RENDER THE FOLDERS -->
            <div v-for="item in documentList" class="document-child">
                <i data-feather="folder" width="80px" height="80px" stroke-width="1"></i>
                <p class="text-instructions">
                    {{shortName("The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog")}}
                </p>
            </div>

            <!-- RENDER THE FILES -->
            <div v-for="item in documentList" class="document-child">
                <i data-feather="file-text" width="80px" height="80px" stroke-width="1"></i>
                <p class="text-instructions">
                    {{shortName("The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog")}}
                </p>
            </div>
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
    export default {
        name: "DocumentsModule",
        props: [
            'destination',
            'location_id',
        ],
        data() {
            return {
                documentList: [1,2,3,4,5,7],
            }
        },
        methods: {
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
        }
    }
</script>

<style scoped>

</style>
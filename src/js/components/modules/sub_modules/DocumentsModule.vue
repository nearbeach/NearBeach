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
        <div v-else>
            ADD CODE!
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
                documentList: [],
            }
        },
    }
</script>

<style scoped>

</style>
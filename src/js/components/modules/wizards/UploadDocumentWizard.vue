<template>
    <div class="modal fade" id="uploadDocumentModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="users"></i> Upload Document Wizard</h2>
                    <button type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            id="uploadDocumentCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    ADD CODE
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button"
                            class="btn btn-primary"
                    >
                        Save changes
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "UploadDocumentWizard",
    props: [
        'currentFolder',
        'destination',
        'locationId',
    ],
    data() {
        return {
            documentModel: [],
            documentDescriptionModel: '',
        };
    },
}
</script>

<style scoped>

</style>
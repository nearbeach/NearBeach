<template>
    <div class="modal fade" id="addBugsModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="users"></i> Add Bugs Wizard</h2>
                    <button type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            id="addBugsCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Adding Bugs</strong>
                            <p class="text-instructions">

                            </p>
                        </div>
                        <div class="col-md-8">

                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-bind:diabled="bugModel == ''"
                            v-on:click="bugModel"
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
        name: "NewBugWizard",
        props: [
            'destination',
            'locationId',
        ],
        data() {
            return {
                bugModel: [],
            }
        }

    }
</script>

<style scoped>

</style>
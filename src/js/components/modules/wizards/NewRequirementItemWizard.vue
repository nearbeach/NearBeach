<template>
    <div class="modal fade"
             id="newItemModal"
             tabindex="-1"
             aria-labelledby="requirementItemModal"
             aria-hidden="true"
    >
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="clipboard"></i> New Requirement Item Wizard</h2>
                    <button type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            id="requirementItemCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Description</strong>
                            <p class="text-instructions">
                                Place in a detailed description of this requirement item.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <label for="id_requirement_item_title">Requirement Item Title:
                                <span class="error" v-if="!$v.requirementItemTitleModel.required"> Please suppy a title.</span>
                            </label>
                            <input id="id_requirement_item_title"
                                   class="form-control"
                                   name="requirement_item_title"
                                   type="text"
                                   required="true"
                                   maxlength="255"
                                   v-model="requirementItemTitleModel"
                            />
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button"
                            class="btn btn-secondary"
                            data-dismiss="modal"
                    >
                        Close
                    </button>
                    <button type="button"
                            class="btn btn-primary"
                            v-on:click="saveItem"
                    >Save Requirement Item</button>
                </div>
            </div>
        </div>
</div>
</template>

<script>
    export default {
        name: "NewRequirementItemWizard",
        props: [],
        data() {
            return {
                requirementItemScopeModel: '',
                requirementItemTitleModel: '',
                stakeholderItemModel: '',
                statusFixList: [],
                statusItemModel: '',
                typeFixList: [],
                typeItemModel: '',
            }
        },
        methods: {
            saveItem: function() {
                //Validate data
            }
        }
    }
</script>

<style scoped>

</style>
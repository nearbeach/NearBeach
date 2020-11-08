<template>
   <div class="modal fade" id="cardInformationModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="users"></i> Card Information</h2>
                    <button type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                            id="cardInformationModalCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Card Text</strong>
                            <p class="text-instructions">Update the card title and then click on "Update Card" button</p>
                        </div>
                        <div class="col-md-8">
                            <label>Card Title</label>
                            <input v-model="cardTitleModel"
                                   class="form-control"
                            >
                            <br/>
                            <button class="btn btn-primary save-changes"
                                    v-on:click="updateCard"
                            >
                                Update Card
                            </button>
                        </div>
                    </div>
                    <hr>

                    <div class="row">
                        <div class="col-md-4">
                            <strong>Comments</strong>
                            <p class="text-instructions">
                                To add a comment - type your comment in the comment box and hit the "Submit Comment"
                                button.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <label>Comment</label>
                            <editor
                               :init="{
                                 height: 250,
                                 menubar: false,
                                 toolbar: 'undo redo | formatselect | ' +
                                  'bold italic backcolor | alignleft aligncenter ' +
                                  'alignright alignjustify | bullist numlist outdent indent | ',
                               }"
                               v-bind:content_css="false"
                               v-bind:skin="false"
                               v-model="cardCommentModel"
                            />
                            <br/>
                            <button class="btn btn-primary save-changes"
                                    v-on:click="updateCard"
                                    v-bind:disabled="cardCommentModel==''"
                            >
                                Submit Comment
                            </button>
                        </div>
                    </div>
                    <hr>

                    <!-- ADD CODE FOR PRIOR COMMENTS -->
                    <div id="card-comments">
                        <!-- PLACE HOLDER IMAGE -->
<!--                        <img alt="Placeholder Image" src="/static/NearBeach/images/placeholder/product_tour.svg">-->
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "CardInformation",
        props: {
            cardId: Number,
            cardTitle: String,
        },
        data() {
            return {
                cardCommentModel: '',
                cardTitleModel: '',
            }
        },
        watch: {
            cardId: function() {

            },
            cardTitle: function() {
                //Update the title
                this.cardTitleModel = this.cardTitle;
            },
        },
        methods: {
            getCardComments: function() {},
            updateCard: function() {
                //ADD CODE
            },
        }
    }
</script>

<style scoped>

</style>
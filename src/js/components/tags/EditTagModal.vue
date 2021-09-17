<template>
    <div class="modal fade" 
         id="editTagModal" 
         data-bs-backdrop="static" 
         data-bs-keyboard="false" 
         tabindex="-1" 
         aria-labelledby="editTagModalLabel" 
         aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="editTagModalLabel">Edit Tag</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Edit Tags</strong>
                            <p class="text-instructions">
                                Please give the tag an appropriate name. Please do not
                                pick an existing tag name.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <label>Tag Name</label>
                            <input class="form-control"
                                   v-model="tagNameModel"
                            >
                        </div>
                    </div>
                    <hr>

                    <div class="row">
                        <div class="col-md-4">
                            <strong>Pick Colour</strong>
                            <p class="text-instructions">
                                Please click on a preferred colour. This will be tags colour.
                            </p>
                        </div>
                        <div class="colour-picker col-md-8">
                            <div v-for="colour in colourList"
                                 v-bind:key="colour"
                                 v-bind:class="getClasses(colour)"
                                 v-bind:style="`background-color: ${colour};`"
                                 v-on:click="updateColour(colour)"
                            ></div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Understood</button>
                </div>
            </div>
        </div>
    </div> 
</template>

<script>
    export default {
        name: 'EditTagModal',
        props: {
            singleTag: Object,
        },
        data() {
            return {
                colourList: [
                    '#37cbd2',
                    '#8b8295',
                    '#6f84bb',
                    '#1fc4b5',
                    '#651794',
                    '#7ea52c',
                    '#6df79e',
                    '#53ef5f',
                    '#79c121',
                    '#91fbde',
                    '#e01059',
                    '#33ae24',
                ],
                tagColourModel: this.singleTag['tagColour'],
                tagNameModel: this.singleTag['tagName'],
            }
        },
        computed: {
        },
        methods: {
            getClasses: function(colour) {
                let return_class = 'single-colour';

                if (colour == this.tagColourModel) {
                    return_class = return_class + ' selected-colour';
                }

                return return_class;
            },
            updateColour: function(selected_colour) {
                this.tagColourModel = selected_colour;
            }
        }   
    }
</script>

<style scoped>
    .single-colour {
        height: 50px;
        width: 50px;
        margin: 6px;
        display: flex;
        justify-content: center;
        align-content: center;
        font-size: larger;
    }

    .colour-picker {
        display: flex;
        flex-wrap: wrap;
    }

    .selected-colour {
        border: 3px solid rgba(51, 51, 51, 0.75);
        background-image: repeating-linear-gradient(45deg, transparent, transparent 3px, rgba(255,255,255,.5) 10px, rgba(255,255,255,.5) 10px);
    }
</style>
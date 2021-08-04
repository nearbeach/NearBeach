<template>
    <div>
        <!-- Card Text -->
        <div class="row">
            <div class="col-md-4">
                <strong>Card Title</strong>
                <p class="text-instructions">
                    Write an appropriate name for the kanban card. To update click on the "Update" button.
                </p>
            </div>
            <div class="col-md-8">
                <label>Card Title</label>
                <input v-model="cardTitleModel"
                        class="form-control"
                >
            </div>
        </div>
        <hr>

        <!-- CARD LOCATION -->
        <div class="row">
            <div class="col-md-4">
                <strong>Card Location</strong>
                <p class="text-instructions">
                    Select the appropriate location for this card.
                </p>
            </div>

            <div class="col-md-8">
                ADD CODE
            </div>
        </div>

        <!-- Update Card -->
        <hr/>
        <button class="btn btn-primary save-changes"
            v-on:click="updateCard"
        >
            Update Card
        </button>
    </div>
</template>

<script>
    import { createHelpers } from 'vuex-map-fields';
    const { mapFields } = createHelpers({
        getterType: 'getCardId',
        mutationType: 'updateCardDetails',
    });

    export default {
        name: 'CardDetails',
        props: {},
        data() {
            return {}
        },
        computed: {
            ...mapFields(['cardTitleModel']),
        },
        methods: {
            updateCard: function() {
                //ADD CODE
            },
        },
    }
</script>

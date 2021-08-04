<template>
    <div>
        <div class="row">
            <div class="col-md-4">
                <strong>Card Description</strong>
                <p class="text-instructions">
                    Fill out a detailed description for the card, then click on the "Update Card" button
                    to update the card.
                </p>
            </div>
            <div class="col-md-8">
                <editor
                    :init="{
                        height: 300,
                        menubar: false,
                        toolbar: 'undo redo | formatselect | ' +
                        'bold italic backcolor | alignleft aligncenter ' +
                        'alignright alignjustify | bullist numlist outdent indent | ',
                    }"
                    v-bind:content_css="false"
                    v-bind:skin="false"
                    v-model="cardDescriptionModel"
                />
            </div>
        </div>
        <hr>
        ADD SAVE BUTTONS
    </div>
</template>

<script>
    export default {
        name: 'CardDescription',
        props: {},
        data() {
            return {}
        },
        computed: {
            cardDescriptionModel: {
                get() {
                    return this.$store.state.cardDescriptionModel;
                },
                set(value) {
                    this.$store.commit({
                        type: 'updateCardDescription',
                        cardDescription: value,
                    })
                }
            }
        },
        methods: {
            updateDescription: function() {
                //ADD CODE
            },
        },
    }
</script>

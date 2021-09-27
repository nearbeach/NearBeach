<template>
    <div class="kanban-row">
        <kanban-card v-for="column in columnResults" :key="column.pk"
                     v-bind:level-id="levelId"
                     v-bind:column-id="column['pk']"
                     v-bind:new-card-info="newCardInfo"
                     v-on:double_clicked_card="doubleClickedCard($event)"
        ></kanban-card>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex';
    
    export default {
        name: "KanbanRow",
        props: {
            //columnResults: Array,
            //kanbanRowModel: Object,
            levelId: Number,
            newCardInfo: Array,
        },
        computed: {
            ...mapGetters({
                columnResults: 'getColumns',
            })
        },
        methods: {
            doubleClickedCard: function(data) {
                //Emit the card id up stream
                this.$emit('double_clicked_card',data);
            },
        }
    }
</script>

<style scoped>

</style>

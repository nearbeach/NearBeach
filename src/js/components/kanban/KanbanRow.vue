<template>
    <div class="kanban-row">
        <kanban-card v-for="column in columnResults"
                     v-bind:master-list="getMasterList(column['pk'])"
                     v-bind:level-id="levelId"
                     v-bind:column-id="column['pk']"
                     v-bind:new-card-info="newCardInfo"
                     v-on:double_clicked_card="doubleClickedCard($event)"
        ></kanban-card>
    </div>
</template>

<script>
    export default {
        name: "KanbanRow",
        props: {
            columnResults: Array,
            kanbanRowModel: Object,
            levelId: Number,
            newCardInfo: Array,
        },
        methods: {
            doubleClickedCard(data) {
                //Emit the card id up stream
                this.$emit('double_clicked_card',data);
            },
            getMasterList: function(row_id) {
                //Determine if the kanban Row exists - if not defined, send back empty array.
                if (this.kanbanRowModel == undefined) {
                    return [];
                }

                //There exists data -> send it back to the user
                return this.kanbanRowModel[row_id];
            }
        }
    }
</script>

<style scoped>

</style>
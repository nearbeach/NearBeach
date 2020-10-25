<template>
    <draggable class="kanban-cell" v-model="localMasterList" groups="tasks" @end="onEnd($event)">
        <div class="list-group-item"
             v-for="card in localMasterList"
             :key="card['pk']"
             :id="card['pk']"
        >
            {{card['fields']['kanban_card_text']}}
        </div>
    </draggable>
</template>

<script>
    export default {
        name: "KanbanCard",
        props: {
            masterList: Array,
        },
        data() {
            return {
                localMasterList: this.masterList,
            }
        },
        methods: {
            onEnd: function(event) {
                console.log("Event: ",event);
            }
        },
        watch: {
            masterList: function() {
                //Update the local master list
                this.localMasterList = this.masterList;
            }
        }
    }
</script>

<style scoped>

</style>
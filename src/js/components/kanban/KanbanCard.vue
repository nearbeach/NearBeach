<template>
    <draggable class="kanban-cell">
        <div class="kanban-card">HOGANS HEROS</div>
    </draggable>
</template>

<script>
    export default {
        name: "KanbanCard",
        props: ['masterList'],
    }
</script>

<style scoped>

</style>
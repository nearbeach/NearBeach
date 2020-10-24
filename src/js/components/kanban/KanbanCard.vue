<template>
    <div class="col-3">
      <h3>Draggable 1</h3>
      <draggable class="list-group" :list="masterList" group="people">
        <div
          class="list-group-item"
          v-for="(element, index) in masterList"
          :key="element.name"
        >
          {{ element.name }} {{ index }}
        </div>
      </draggable>
    </div>
</template>

<script>
    export default {
        name: "KanbanCard",
        props: ['masterList'],
    }
</script>

<style scoped>

</style>
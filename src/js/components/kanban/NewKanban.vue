<template>
    <div class="card">
        <div class="card-body">
            <h1>New Kanban</h1>
            <hr>

            <div class="row">
                <!-- DESCRIPTION -->
                <div class="col-md-4">
                    <strong>Please note</strong>
                    <p class="text-instructions">
                        Board names must be unique.
                    </p>
                </div>

                <!-- BOARD NAME -->
                <div class="col-md-8">
                    <div class="form-group">
                        <label>Kanban Board Name</label>
                        <input type="text"
                               v-model="kanbanBoardNameModel">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "NewKanban",
        props: {},
        data() {
            return {
                kanbanBoardNameModel: '',
            }
        }
    }
</script>

<style scoped>

</style>
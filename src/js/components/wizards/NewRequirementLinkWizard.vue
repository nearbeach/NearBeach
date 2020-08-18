<template>
    <div class="modal-body">
        <h3>Object Selector</h3>
        <p class="text-instructions">
            Please select which object you would like to link to this requirement.
        </p>
        <v-select :options="['Project','Tasks','Opportunities']"></v-select><!-- TEMP CODE -->
    </div>
</template>

<script>
    export default {
        name: "NewRequirementLinkWizard"
    }
</script>

<style scoped>

</style>
<template>
    <div class="card">
        <h1>New Requirement</h1>
        <hr>
        <div class="grid-x">
            <!-- Description -->
            <div class="small-12 large-4">
                <strong>Description</strong><br/>
                <p>Place a basic helicopter view of the requirement description here. You will be able to break this
                    description down into smaller items using the requirement items below.</p>
            </div>
            <div class="small-12 large-8">
                <editor
                   :init="{
                     height: 500,
                   }"
                 />
            </div>

            <!-- Status -->
            <hr>
            <div class="small-12 large-4">
                <strong>Status</strong><br/>
                <p>Set the Requirement Status here.</p>
            </div>
            <div class="small-12 large-4">
                <label>Requirement Type
                    <v-select :options="[{label: 'Canada', code: 'ca'}]"></v-select>
                </label>
            </div>
            <div class="small-12 large-4">
                <label>Requirement Type
                    <v-select :options="[{label: 'Canada', code: 'ca'}]"></v-select>
                </label>
            </div>

            <!-- Group Permissions -->
            <hr>
            <group-permissions></group-permissions>

            <!-- Submit Button -->
            <hr>
            <div class="cell medium-12 large-12">
                <a href="#" class="button save-changes">Save Changes</a>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript components
    import Editor from '@tinymce/tinymce-vue';
    import vSelect from "vue-select";

    //Vue components
    import GroupPermissions from '../permissions/GroupPermissions.vue';

    export default {
        name: "NewRequirement",
        components: {
            Editor,
            vSelect,
            GroupPermissions,
        }
    }
</script>

<style scoped>

</style>
<template>
    <div class="grid-x">
        <div class="small-12 large-4">
            <h3>Group Permissions</h3>
            <p>Add or remove groups from this requirement. Adding a group will allow users
                from that group to access this requirement.
            </p>
            <p>If you do not add one of your own group(s), you will only get readonly access.</p>
        </div>
        <div class="small-12 large-8">
            <label>Group List
                <v-select :options="groupFixResults"
                          label="group"
                          v-model="groupModel"
                          multiple
                    ></v-select>
            </label>
        </div>
    </div>
</template>

<script>
    import vSelect from "vue-select";

    export default {
        name: "GroupPermissions",
        components: {
            vSelect,
        },
        props: [
            'groupResults',
        ],
        data() {
            return {
                'groupFixResults': [],
                'groupModel': [],
            }
        },
        mounted() {
            //Fix up the list to remove any django nested loops
            this.groupResults.forEach((row) => {
                //Construct the object
                var construction_object = {
                    'value': row['pk'],
                    'group': row['fields']['group_name'],
                }

                //Push the object to type fix list
                this.groupFixResults.push(construction_object);
            });
        }
    }
</script>

<style scoped>

</style>
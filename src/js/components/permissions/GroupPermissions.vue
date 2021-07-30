<template>
    <div class="row">
        <div class="col-md-4">
            <h2>Group Permissions</h2>
            <p class="text-instructions">
                Add or remove groups from this {{destination}}. Adding a group will allow users
                from that group to access this {{destination}}.
            </p>
            <p class="text-instructions">
                If you do not add one of your own group(s), you will only get readonly access.
            </p>
        </div>
        <div class="col-md-8">
            <label>Group List
                <span class="error" v-if="!$v.groupModel.required && isDirty"> Please select at least one group.</span>
            </label>
            <v-select :options="groupFixResults"
                      label="group"
                      v-model="groupModel"
                      multiple
            ></v-select>
        </div>
    </div>
</template>

<script>
    //Validation
    import { required } from 'vuelidate/lib/validators'

    export default {
        name: "GroupPermissions",
        components: {},
        props: {
            destination: String,
            groupResults: Array,
            isDirty: Boolean, //Passes the value from the template above where the checking is done
            userGroupResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        watch: {
            'groupModel': function() {
                //Send the data upstream
                this.$emit('update_group_model',this.groupModel);
            }
        },
        data() {
            return {
                'groupFixResults': [],
                'groupModel': [],
            }
        },
        validations: {
            groupModel: {
                required,
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

            //Any User groups are added to the group Model
            this.groupModel = this.userGroupResults.map(row => {
                return {
                    group: row['group__group_name'],
                    value: row['group_id'],
                }
            });
        }
    }
</script>

<style scoped>

</style>

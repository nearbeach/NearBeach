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
                <span class="error" v-if="!v$.groupModel.required && isDirty"> Please select at least one group.</span>
            </label>
            <n-select :options="groupFixResults"
                      label="group"
                      v-model:value="groupModel"
                      multiple
            ></n-select>
        </div>
    </div>
</template>

<script>
    //Validation
    import useVuelidate from '@vuelidate/core'
    import { required } from '@vuelidate/validators'
    import { NSelect } from 'naive-ui';

    export default {
        name: "GroupPermissions",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            NSelect,
        },
        props: {
            destination: {
                type: String,
                default: '',
            },
            groupResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            isDirty: {
                type: Boolean,
                default: true,
            }, //Passes the value from the template above where the checking is done
            userGroupResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        watch: {
            groupModel: function() {
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
            this.groupFixResults = this.groupResults.map((row) => {
                return {
                    value: row.pk,
                    label: row.fields.group_name,
                }
            });

            //Any User groups are added to the group Model
            this.groupModel = this.userGroupResults.map(row => {
                return row.group_id;
            });
        }
    }
</script>

<style scoped>

</style>

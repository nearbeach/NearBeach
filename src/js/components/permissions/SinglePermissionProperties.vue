<template>
    <div class="row">
        <label>{{propertyLabel}}</label>
        <v-select :options="fixListOfChoices"
                  v-model="propertyModel"
                  class="form-group"
        ></v-select>
    </div>
</template>

<script>
export default {
    name: "SinglePermissionProperties",
    props: {
        property: String,
        propertyLabel: String,
        propertyValue: {
            Type: Number,
            default: 0
        },
        listOfChoices: Array,
    },
    data() {
        return {
            propertyModel: {
                'label': this.getLabel(this.propertyValue),
                'value': this.propertyValue,
            },
            fixListOfChoices: [],
        }
    },
    watch: {
        propertyModel: function() {
            //If there are no values - use the default value
            if (this.propertyModel === null) {
                //Define the default of 0
                this.propertyModel = {
                    'label': this.getLabel(0),
                    'value': 0,
                }
            }

            // Send the new property value up stream
            this.$emit('update_property_value',{
                'property': this.property,
                'value': this.propertyModel['value'],
            });
        },
    },
    methods: {
        getLabel: function(input_data) {
            //Use the input data to filter the list of choices, to object the label
            const filtered_value = this.listOfChoices.filter(row => {
                return row[0] === input_data;
            });

            //Make sure there is a value, or send back  ""
            if (filtered_value.length === 0) {
                return "";
            }

            //Return the value at [0][1]
            return filtered_value[0][1];
        }
    },
    mounted() {
        //We need to fix the list of choices, so the trupal has the value, label fields defined
        this.fixListOfChoices = this.listOfChoices.map(row => {
            return {
                'label': row[1],
                'value': row[0],
            };
        });
    }
}
</script>

<style scoped>

</style>
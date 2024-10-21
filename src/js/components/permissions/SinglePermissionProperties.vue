<template>
	<div class="row">
		<label>{{ propertyLabel }}</label>
		<n-select
			:options="fixListOfChoices"
			v-model:value="propertyModel"
		></n-select>
	</div>
</template>

<script>
import {NSelect} from "naive-ui";

export default {
	name: "SinglePermissionProperties",
	components: {
		NSelect,
	},
	emits: [
		'update_property_value',
	],
	props: {
		property: {
			type: String,
			default: "",
		},
		propertyLabel: {
			type: String,
			default: "",
		},
		propertyValue: {
			type: Number,
			default: 0,
		},
		listOfChoices: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	data() {
		return {
			propertyModel: this.propertyValue,
			fixListOfChoices: [],
		};
	},
	watch: {
		propertyModel() {
			//If there are no values - use the default value
			if (this.propertyModel === null) {
				//Define the default of 0
				this.propertyModel = 0;
			}

			// Send the new property value up stream
			this.$emit("update_property_value", {
				property: this.property,
				value: this.propertyModel,
			});
		},
	},
	methods: {
		getLabel(input_data) {
			//Use the input data to filter the list of choices, to object the label
			const filtered_value = this.listOfChoices.filter((row) => {
				return row[0] === input_data;
			});

			//Make sure there is a value, or send back  ""
			if (filtered_value.length === 0) {
				return "";
			}

			//Return the value at [0][1]
			return filtered_value[0][1];
		},
	},
	mounted() {
		//We need to fix the list of choices, so the trupal has the value, label fields defined
		this.fixListOfChoices = this.listOfChoices.map((row) => {
			return {
				label: row[1],
				value: row[0],
			};
		});
	},
};
</script>



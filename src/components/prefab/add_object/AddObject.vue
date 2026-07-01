<script setup lang="ts">
import {WlkFormGroup} from "whelk-ui";
import {computed, type PropType, useId} from "vue";

// DEFINE PROPS
const props = defineProps({
	label: {
		type: String,
		required: true,
	},
	options: {
		type: Array as PropType<{ [key: string]: unknown }[]>,
		required: true,
	},
	optionsLabel: {
		type: String,
		required: false,
		default: 'label',
	},
	optionsValue: {
		type: String,
		required: false,
		default: 'value',
	},
});

// Define model
const model = defineModel({required: true})

// Define computed
const componentId = computed<string>(() => {
	// Return an id made up of input- + title
	return props.label?.toLowerCase()?.replace(/ /g, '-') + "-" + useId();
});

const isDisabled = computed<boolean>(() => {
	return props.options?.length === undefined || props.options?.length === 0;
})

// Define functions
function getKeys(value: unknown, index: number): string {
	if (typeof value === "string" || typeof value === "number") {
		return value.toString();
	}

	return index.toString();
}

function onFocus($event: FocusEvent) {
	// Check for user activation
	if (!navigator.userActivation.isActive) {
		// Nothing to do
		return;
	}

	// Show the picker
	const target = $event.target as HTMLInputElement;
	target.showPicker();
}
</script>

<template>
	<WlkFormGroup class="add-object">
		<label :for="componentId">+{{ label }}</label>
		<select
			:disabled="isDisabled"
			:id="componentId"
			:name="props.label"
			v-model="model"
			@focus="onFocus"
		>
			<option
				v-for="(option, index) in options"
				:key="getKeys(option[optionsValue], index)"
				:value="option[optionsValue]"
			>{{ option[optionsLabel] }}
			</option>
		</select>

	</WlkFormGroup>
</template>

<style scoped>
.add-object {
	> label {
		display: inline-block;
		width: 100%;
		text-align: center;
		transform: translateY(29px);
		font-family: "Roboto", sans-serif;
		font-weight: lighter;
		font-size: 0.75rem;
	}

	> select {
		width: 100%;
		border-style: dashed;
		border-width: var(--border-width);
		border-radius: var(--border-radius);
		padding: 0.5rem 0.75rem;
		font-weight: lighter;
		font-size: 1rem;
		color: #0000;
	}
}


</style>
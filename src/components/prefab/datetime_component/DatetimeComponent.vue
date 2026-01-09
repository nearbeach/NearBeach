<script setup lang="ts">
import FormGroup from '@/components/prefab/form_group/FormGroup.vue';
import {computed, ref} from 'vue';
import RenderErrorMessage from '@/components/prefab/error/RenderErrorMessage.vue';
import TooltipComponent from '@/components/prefab/tooltip_component/TooltipComponent.vue';

// Define Emits
const emit = defineEmits(['isValid']);

// Define Props
const props = defineProps({
	isRequired: {
		type: Boolean,
		default: false,
	},
	label: {
		type: String,
		required: true,
	},
	tooltipMessage: {
		type: String,
		required: false,
		default: '',
	},
	tooltipTitle: {
		type: String,
		required: false,
		default: '',
	},
});

// Define Models
const model = defineModel('model', {
	type: Date,
	required: false,
});

// Define ref
const hasError = ref(false);
const errorMessage = ref('');

// Computed
const getId = computed(() => {
	// Return an id made up of input- + title
	return 'input-' + props.label?.toLowerCase()?.replace(' ', '-');
});

function checkValidation() {
	// Fall back to defaults
	hasError.value = false;
	errorMessage.value = '';

	// Get the length of the model and if NaN fallback to 0
	let modelLength: number = Number(model?.value?.toString().length);
	modelLength = isNaN(modelLength) ? 0 : modelLength;

	// Check the first "required" condition
	if (props.isRequired && modelLength === 0) {
		hasError.value = true;
		errorMessage.value = 'This field is required';
	}

	// Set the defined ref and tell parent
	emit('isValid', !hasError.value);
}
</script>

<template>
	<FormGroup class="datetime-component">
		<label :for="getId">
			<TooltipComponent
				v-if="props.tooltipMessage !== ''"
				:title="tooltipTitle"
				:message="tooltipMessage"
				:id="getId"
			/>
			{{
				label
			}}<span v-if="isRequired" aria-description="Field is required"
		>*</span
		>
		</label>
		<input
			:id="getId"
			type="datetime-local"
			:name="props.label"
			v-model="model"
			v-on:keyup="checkValidation"
			v-on:focusout="checkValidation"
		/>
		<RenderErrorMessage :error-message="errorMessage"/>
	</FormGroup>
</template>

<style scoped>
.datetime-component {

	label {
		margin-bottom: 6px;
	}

	span {
		color: var(--text-red);
	}

	input {
		border-style: var(--border-style);
		border-width: var(--border-width);
		border-radius: var(--border-radius);
		border-color: var(--border);
		box-sizing: border-box;
		-moz-box-sizing: border-box;
		-webkit-box-sizing: border-box;

		&:focus {
			border-color: var(--secondary);
			border-width: 2px;
			outline: none;
			padding: calc(0.5rem - 1px);
		}
	}

	&.compact {
		> label {
			font-size: 1rem;
			line-height: 1.25rem;
			margin-bottom: 2px;

			@media (--large-screen) {
				font-size: 0.75rem;
				line-height: 1rem;
			}
		}

		> input {
			font-size: 1.25rem;
			line-height: 1.5rem;
			padding: 0.25rem;

			@media (--large-screen) {
				font-size: 1rem;
				line-height: 1.25rem;
			}
		}
	}
}
</style>

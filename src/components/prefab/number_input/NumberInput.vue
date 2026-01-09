<script setup lang="ts">
import FormGroup from '@/components/prefab/form_group/FormGroup.vue';
import {computed, ref} from 'vue';
import TooltipComponent from '@/components/prefab/tooltip_component/TooltipComponent.vue';
import RenderErrorMessage from "@/components/prefab/error/RenderErrorMessage.vue";

// Define Props
const props = defineProps({
	label: {
		type: String,
		required: true,
	},
	maxValue: {
		type: Number,
		default: Number.MAX_SAFE_INTEGER,
	},
	minValue: {
		type: Number,
		default: Number.MIN_SAFE_INTEGER,
	},
	stepIncrement: {
		type: Number,
		default: 1,
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
const model = defineModel({
	type: Number,
	default: 0,
});

// Define Ref
const errorMessage = ref('');

// Computed
const getId = computed(() => {
	// Return an id made up of input- + title
	return 'input-' + props.label?.toLowerCase()?.replace(' ', '-');
});

const isMax = computed(() => {
	return model.value >= props.maxValue;
});

const isMin = computed(() => {
	return model.value <= props.minValue;
});

// FUNCTIONS
function applyDecrement() {
	// Reset error messages
	errorMessage.value = '';

	// Do nothing if we reach the lowest value
	if (isMin.value) {
		errorMessage.value = "Reached Lowest Value";
		return;
	}

	// We don't want to increment past the min value - so we define a local increment
	let increment = Math.abs(props.minValue - model.value);
	increment =
		increment < Math.abs(props.stepIncrement)
			? increment
			: Math.abs(props.stepIncrement);

	// Apply the incrementation, and make sure it is not bigger than the max value
	let update_value = model.value - increment;
	update_value =
		update_value > props.maxValue ? props.maxValue : update_value;

	//Mutate the value
	model.value = update_value;
}

function applyIncrement() {
	// Reset error messages
	errorMessage.value = '';

	// Do nothing if we reach the highest value
	if (isMax.value) {
		errorMessage.value = "Reached Maxium Value";
		return;
	}

	// We don't want to increment past the max value - so we define a local increment
	let increment = Math.abs(props.maxValue - model.value);
	increment =
		increment < Math.abs(props.stepIncrement)
			? increment
			: Math.abs(props.stepIncrement);

	// Apply the incrementation, and make sure it is not lower than the min value
	let update_value = model.value + increment;
	update_value =
		update_value < props.minValue ? props.minValue : update_value;

	// Mutate the value
	model.value = update_value;
}

function manualUpdate(event: Event) {
	// Reset error messages
	errorMessage.value = '';

	// Handle manual event
	const target = event.target as HTMLInputElement;
	let update_value: number | undefined = target?.valueAsNumber;
	if (update_value === undefined) {
		errorMessage.value = "Model is undefined - default 0";
		update_value = 0;
	}
	if (isNaN(update_value)) {
		errorMessage.value = "Not a number - default 0";
		update_value = 0;
	}


	// Make sure the values fall within the min and max
	update_value =
		update_value > props.maxValue ? props.maxValue : update_value;
	update_value =
		update_value < props.minValue ? props.minValue : update_value;

	// Mutate the value
	model.value = update_value;
}
</script>

<template>
	<FormGroup class="number-input">
		<label :for="getId">
			<TooltipComponent
				v-if="props.tooltipMessage !== ''"
				:title="tooltipTitle"
				:message="tooltipMessage"
				:id="getId"
			/>
			{{ label }}
		</label>
		<div class="number-input-row">
			<button
				type="button"
				class="negative"
				v-bind:aria-label="`Decrement current value of ${model} by ${props.stepIncrement}`"
				v-bind:disabled="isMin"
				v-on:click="applyDecrement"
			>
				-
			</button>
			<input
				type="number"
				aria-label="Current value picked"
				aria-describedby="helper-text-explanation"
				v-model="model"
				v-on:change="manualUpdate($event)"
				v-on:keyup="manualUpdate($event)"
			/>
			<button
				type="button"
				class="positive"
				v-bind:aria-label="`Increment current value of ${model} by ${props.stepIncrement}`"
				v-bind:disabled="isMax"
				v-on:click="applyIncrement"
			>
				+
			</button>
		</div>
		<RenderErrorMessage :error-message="errorMessage"/>
	</FormGroup>
</template>

<style scoped>
.number-input {
	> label {
		margin-bottom: 6px;
	}

	> .number-input-row {
		display: grid;
		grid-template-columns: 3rem minmax(0, 1fr) 3rem;

		> .negative {
			border-radius: var(--border-radius) 0 0 var(--border-radius);
			border-width: var(--border-width) 0 var(--border-width) var(--border-width);
		}

		> input {
			border-style: var(--border-style);
			border-width: var(--border-width);
			border-radius: 0;
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

		> .positive {
			border-radius: 0 var(--border-radius) var(--border-radius) 0;
			border-width: var(--border-width) var(--border-width) var(--border-width) 0;
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

		> .number-input-row {
			grid-template-columns: 2.5rem minmax(0, 1fr) 2.5rem;

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
}

/* Hide the spin buttons in WebKit browsers */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
	-webkit-appearance: none;
	margin: 0;
}

/* Hide spin buttons in Firefox */
input[type='number'] {
	-moz-appearance: textfield;
}
</style>

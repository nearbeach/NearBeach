<script setup lang="ts">
import {computed} from "vue";
import FormGroup from "@/components/prefab/form_group/FormGroup.vue";
import TooltipComponent from "@/components/prefab/tooltip_component/TooltipComponent.vue";

// Define props
const props = defineProps({
	label: {
		type: String,
		required: true,
	},
	offText: {
		type: String,
		required: false,
		default: "",
	},
	onText: {
		type: String,
		required: false,
		default: "",
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
})

// Define computed
const getClass = computed(() => {
	return model.value ? "switch on" : "switch off";
});

const getId = computed(() => {
	// Return an id made up of input- + title
	return 'input-' + props.label?.toLowerCase()?.replace(' ', '-');
});

const getText = computed(() => {
	return model.value ? props.onText : props.offText;
});

// Define model
const model = defineModel({
	type: Boolean
});

// Define functions
function switchClicked() {
	model.value = !model.value;
}
</script>

<template>

	<FormGroup class="switch-component">
		<label :for="getId">
			<TooltipComponent
				v-if="props.tooltipMessage !== ''"
				:title="tooltipTitle"
				:message="tooltipMessage"
				:id="getId"
			/>
			{{
				label
			}}
		</label>
		<div
			v-on:click="switchClicked"
			:class="getClass"
		>
			<div class="switch-text">{{ getText }}</div>
			<div class="switch-block"></div>
		</div>
	</FormGroup>
</template>

<style scoped>
.switch-component {
	width: 100%;

	> .switch {
		display: grid;
		grid-template-columns: [on] 2rem [text] minmax(0, 1fr) [off] 2rem;
		border-style: var(--border-style);
		border-width: var(--border-width);
		border-radius: var(--border-radius);
		border-color: var(--border);
		box-sizing: border-box;
		-moz-box-sizing: border-box;
		-webkit-box-sizing: border-box;

		> .switch-block {
			width: 2rem;
			height: 2rem;
			background-color: hotpink;
		}

		> .switch-text {
			display: grid;
			grid-area: text;
			text-align: center;
			align-items: center;
			overflow: hidden;
			white-space: nowrap;
			text-overflow: ellipsis;
		}

		&.on {
			> .switch-block {
				grid-area: on;
				background-color: var(--success);
			}
		}

		&.off {
			> .switch-block {
				grid-area: off;
				background-color: var(--info);
			}
		}
	}

	&.compact {
		> label {
			font-size: 1rem;
			line-height: 1.25rem;
		}

		> .switch {

			grid-template-columns: [on] 1rem [text] minmax(0, 1fr) [off] 1rem;

			> .switch-block {
				width: 1rem;
				height: 1rem;
			}

			> .switch-text {
				font-size: 0.75rem;
				line-height: 1rem;
			}
		}
	}
}

</style>
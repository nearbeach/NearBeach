<script setup lang="ts">
import {ref} from 'vue'
import ButtonComponent from "@/components/prefab/button/ButtonComponent.vue";
import {ButtonVariantEnum} from '@/utils/enums/ButtonVariantEnum.ts';
import {ObjectStateEnum} from '@/utils/enums/ObjectStateEnum.ts';

// DEFINE EMITS
const emit = defineEmits(['removeOrganisation']);

// DEFINE PROPS
const props = defineProps({
	organisationId: {
		type: Number,
		required: true,
	},
	organisationName: {
		type: String,
		required: true,
	}
})

// DEFINE REF
const removeOrganisationState = ref(ObjectStateEnum.NoAction)

// DEFINE METHODS
function removeOrganisation() {
	emit('removeOrganisation');
}
</script>

<template>
	<div class="stakeholder-organisation">
		<p class="stakeholder-organisation-name">Organisation</p>
		<p class="stakeholder-organisation-link">
			<RouterLink :to="`organisation/${organisationId}`">
				{{ props.organisationName }}
			</RouterLink>
		</p>
		<ButtonComponent
			class="tiny"
			label="Remove Organisation"
			:variant="ButtonVariantEnum.Danger"
			:objectState="removeOrganisationState"
			v-on:click="removeOrganisation"
		/>
	</div>
</template>

<style scoped>
.stakeholder-organisation {
	> .stakeholder-organisation-name {
		font-size: 0.75rem;
		line-height: 1rem;
	}

	> .stakeholder-organisation-link {
		font-size: 0.75rem;
		line-height: 1rem;
		margin: 0 0 1rem 0;
	}
}
</style>
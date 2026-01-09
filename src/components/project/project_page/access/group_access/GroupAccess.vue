<script setup lang="ts">

import {ObjectTitleCaseEnums} from "@/utils/enums/ObjectTitleCaseEnums.ts";
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import type {PropType} from "vue";
import {TrashIcon} from "lucide-vue-next";

// DEFINE EMITS
const emit = defineEmits([
	'removeGroup',
]);

// DEFINE PROPS
const props = defineProps({
	groupList: {
		type: Array as PropType<{ group_id: number, group_name: string }[]>,
		required: true,
	},
});

// DEFINE FUNCTIONS
function removeGroup(group_id: number) {
	emit('removeGroup', group_id);
}
</script>

<template>
	<div class="group-access">
		<h3>Group Access</h3>
		<div
			v-if="props.groupList.length > 0"
			class="group-access-list"
		>
			<div
				v-for="group in props.groupList"
				:key="group.group_id"
				class="group-access-item"
			>
				<p>{{ group.group_name }}</p>
				<TrashIcon
					v-if="props.groupList.length > 1"
					v-on:click="removeGroup(group.group_id)"
					type="button"
					aria-label="Remove group"
				/>
			</div>
		</div>

		<AddObject
			:object-type="ObjectTitleCaseEnums.group"
		/>
	</div>
</template>

<style scoped>
.group-access {

	> .group-access-list {
		> .group-access-item {
			padding: 0.5rem 0;
			display: grid;
			grid-template-columns: [name] minmax(0, 1fr) [icon] 20px;

			> p {
				grid-area: name;
				overflow: hidden;
				white-space: nowrap;
				text-overflow: ellipsis;
				padding: 0;
				margin: 0;
				font-size: 1rem;
			}

			> svg {
				grid-area: icon;
				width: 20px;
				height: 20px;
			}

			&:hover {
				background-color: var(--secondary-hover);
			}
		}
	}

	> .add-object {
		margin: 1rem 0;
	}
}

</style>
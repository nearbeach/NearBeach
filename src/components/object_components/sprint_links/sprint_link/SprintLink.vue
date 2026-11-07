<script setup lang="ts">
import type {SprintLinkInterface} from "@/utils/interfaces/SprintLinkInterface.ts";
import {WlkCard} from "whelk-ui";
import {TrashIcon} from "@lucide/vue";
import {computed} from "vue";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Define emits
const emits = defineEmits(['deleteSprint']);

// Define stores
const permissionStore = usePermissionStore();

// Define props
const props = defineProps({
	index: {
		type: Number,
		required: true,
	},
	sprint: {
		type: Object as () => SprintLinkInterface,
		required: true,
	},
});

// Define computed
const renderDates = computed(() => {
	const start_date = props.sprint?.start_date?.split("T")[0] ?? "";
	const end_date = props.sprint?.end_date?.split("T")[0] ?? "";

	return `${start_date} - ${end_date}`;
})
</script>

<template>
	<WlkCard class="sprint-link">
		<div class="sprint-description">
			<div class="sprint-title">
				<a target="_blank"
				   rel="noopener noreferrer"
				   :href="`/sprint/${sprint.id}/`"
				>
					{{ sprint.title }}
				</a>
			</div>
			<div class="sprint-information">{{sprint.status}} - <span class="dates">{{renderDates}}</span></div>
		</div>
		<div class="sprint-delete"
		     v-if="permissionStore.currentObjectPermissions.currentObject > 1"
		>
			<TrashIcon v-on:click="emits('deleteSprint', sprint.id)" />
		</div>
	</WlkCard>
</template>

<style scoped>
.sprint-link {
	display: flex;
	flex-direction: row;
	padding: 0.75rem 0.5rem;

	> .sprint-description {
		width: calc(100% - 20px);

		> .sprint-title {
			font-weight: bolder;
			font-size: 1rem;
		}

		> .sprint-information {
			font-weight: bold;
			font-size: 0.75rem;

            > .dates {
                font-weight: lighter;
            }
		}
	}

	> .sprint-delete {
		width: 20px;

		> svg {
			width: 20px;
			height: 20px;
		}
	}
}
</style>
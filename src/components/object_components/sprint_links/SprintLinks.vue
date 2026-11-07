<script setup lang="ts">
import {computed, onMounted, ref, watch} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {
	WlkButton,
	WlkDate,
	WlkModal,
	WlkModalFooter,
	WlkModalHeader,
	WlkRenderErrorMessage,
	WlkTextInput
} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import type {SprintLinkInterface} from "@/utils/interfaces/SprintLinkInterface.ts";
import {X} from "@lucide/vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {safeFetch} from "@/composables/safeFetch.ts";
import SprintLink from "@/components/object_components/sprint_links/sprint_link/SprintLink.vue";
import {useErrorStore} from "@/stores/error/error.ts";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Define i18n
const {t} = useI18n()

// Define stores
const errorStore = useErrorStore();
const objectStore = useObjectStore();
const permissionStore = usePermissionStore();

// Define refs
const errorMessage = ref<string>("");
const modalClass = ref<string>("");
const sprintData = ref<SprintLinkInterface[]>([]);
const sprintTitleModel = ref("");
const sprintEndDateModel = ref("");
const sprintStartDateModel = ref("");

// Define watch
watch(
	() => objectStore.is_loaded,
	async (new_value) => {
		// If object data is now loaded - fetch data
		if (new_value) {
			await loadData();
		}
	}
);

// Define computed
const disableCreateSprint = computed(() => {
	// Set up a set that we'll remove from potential results
	const existingTitlesSet = new Set(sprintData.value.map(x => x.title));

	// Return
	return existingTitlesSet.has(sprintTitleModel.value);
})

// Define onMounted
onMounted(async () => {
	if (objectStore.is_loaded) {
		await loadData();
	}
});

// Define computed
const listCurrentSprints = computed(() => {
	// Condition end date >= current date
	const current_date = new Date();

	return sprintData.value.filter((row) => {
		// Get the date
		const date = new Date(row.end_date);

		// Return condition || undefine date
		return date === undefined || date.getTime() >= current_date.getTime();
	});
});

const listPastSprints = computed(() => {
	// Condition end date < current date
	const current_date = new Date();

	return sprintData.value.filter((row) => {
		// Get the date
		const date = new Date(row.end_date);

		// Return condition || undefined date
		return date === undefined || date.getTime() < current_date.getTime();
	});
});

// Define functions
function closeModal() {
	modalClass.value = "";
}

async function createSprint() {
	// TODO - validate fields before sending data

	const body = {
		title: sprintTitleModel.value,
		end_date: sprintEndDateModel.value,
		start_date: sprintStartDateModel.value,
	};

	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/sprint/`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		},
	);

	// Close the modal
	closeModal();

	switch (response.status) {
		case 201: {
			const data = await response.json();
			sprintData.value.push(data);
			break;
		}
		case 403:
			errorStore.setError(t("general_detail_component.error_forbidden"));
			errorStore.showErrorModal = true;
			break;
		default:
			errorStore.setError(response.statusText);
			errorStore.showErrorModal = true;
			break;
	}
}

async function deleteSprint(sprint_id: string) {
	// Set backup
	const backup = sprintData.value;

	// Remove from list
	sprintData.value = sprintData.value.filter((sprint) => {
		return sprint.id !== sprint_id;
	});

	// Update backend
	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/sprint/${sprint_id}/`,
		{
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			}
		}
	)

	switch (response.status) {
		case 204:
			break;
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			sprintData.value = backup;
			break;
		default:
			errorMessage.value = response.statusText;
			sprintData.value = backup;
			break;
	}
}

async function loadData() {
	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/sprint/`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			}
		}
	)

	switch (response.status) {
		case 200: {
			const data = await response.json();
			sprintData.value = data;
			break;
		}
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			break;
		default:
			errorMessage.value = response.statusText;
			break;
	}
}

function openModal() {
	// Get start date
	const date = new Date();
	const start_date = date.toISOString().split("T")[0] ?? "";
	sprintStartDateModel.value = start_date;

	// Get end date
	date.setDate(date.getDate() + 7);
	const end_date = date.toISOString().split("T")[0] ?? "";
	sprintEndDateModel.value = end_date;

	// Set the title
	sprintTitleModel.value = `${objectStore.destination}-${objectStore.id}: ${start_date} -> ${end_date}`;

	// Open Modal
	modalClass.value = "open";
}
</script>

<template>
	<div class="sprint-links">
		<h3>{{ t("sprint_links.sprint_title") }}</h3>
		<p class="sub-text">{{ t("sprint_links.description") }}</p>
		<div class="empty-sprint-list"
		     v-if="sprintData.length === 0"
		>
			{{ t("sprint_links.empty_sprint_links") }}
		</div>

		<WlkRenderErrorMessage>{{errorMessage}}</WlkRenderErrorMessage>

		<h3 v-if="listCurrentSprints.length > 0">Current Sprints</h3>
		<div class="sprint-list"
		     v-if="listCurrentSprints.length > 0"
		>
			<SprintLink v-for="(sprint, index) in listCurrentSprints"
			            :index="index"
			            :key="sprint.id"
			            :sprint="sprint"
			            v-on:delete-sprint="deleteSprint"
			/>
		</div>

		<h3 v-if="listPastSprints.length > 0">Past Sprints</h3>
		<div class="sprint-list"
		     v-if="listPastSprints.length > 0"
		>
			<SprintLink v-for="(sprint, index) in listPastSprints"
			            :index="index"
			            :key="sprint.id"
			            :sprint="sprint"
			            v-on:delete-sprint="deleteSprint"
			/>
		</div>

		<div class="sprint-buttons"
			 v-if="permissionStore.currentObjectPermissions.currentObject > 1"
		>
			<WlkButton class="compact primary"
			           @click="openModal"
			>
				{{ t("sprint_links.create_sprint") }}
			</WlkButton>
		</div>
	</div>

	<teleport to="body">
		<WlkModal :class="modalClass">
			<WlkModalHeader>
				<div class="modal-header-row">
					<h3>{{ t("sprint_links.create_sprint") }}</h3>
					<X :size="20"
					   :aria-label="t('sprint_links.close_modal')"
					   v-on:click="closeModal"
					/>
				</div>
			</WlkModalHeader>

			<WlkTextInput :label="t('sprint_links.modal_sprint_title')" v-model="sprintTitleModel"/>
			<div class="date-row">
				<WlkDate :label="t('sprint_links.modal_start_date')" v-model="sprintStartDateModel"/>
				<WlkDate :label="t('sprint_links.modal_end_date')" v-model="sprintEndDateModel"/>
			</div>

			<WlkModalFooter class="modal-footer-row">
				<WlkButton class="compact secondary"
				           v-on:click="closeModal"
				>{{ t("sprint_links.close_modal") }}
				</WlkButton>
				<WlkButton class="compact primary"
				           :disabled="disableCreateSprint"
				           v-on:click="createSprint"
				>{{ t("sprint_links.create_sprint") }}
				</WlkButton>
			</WlkModalFooter>

		</WlkModal>
	</teleport>
</template>

<style scoped>
.sprint-links {
	> .sprint-buttons {
		padding-top: 0.75rem;
	}

	> .empty-sprint-list {
		margin-top: 2rem;
		height: 7rem;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.25rem;
		font-weight: 100;
		font-family: "Roboto", sans-serif;
		border: dashed;
		border-radius: var(--border-radius);
		border-width: var(--border-width);
	}
}

.modal-header-row,
.modal-footer-row {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
}

.date-row {
	display: flex;
	flex-direction: row;

	> .wlk-date {
		width: 50%;
	}

	> .wlk-date:nth-child(1) {
		margin-right: 0.125rem;
	}

	> .wlk-date:nth-child(2) {
		margin-left: 0.125rem;
	}
}
</style>
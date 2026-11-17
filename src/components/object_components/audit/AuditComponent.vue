<script setup lang="ts">
import {WlkButton} from "whelk-ui";
import {onMounted, ref, watch} from "vue";
import {useI18n} from "petite-vue-i18n";
import type {AuditLogItemInterface, AuditLogPageInterface} from "@/utils/interfaces/AuditLogItemInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {safeFetch} from "@/composables/safeFetch.ts";
import {useErrorStore} from "@/stores/error/error.ts";

// Define i18n
const {t} = useI18n();

// Define stores
const errorStore = useErrorStore();
const objectStore = useObjectStore();

// Define ref
const auditList = ref<AuditLogItemInterface[]>([]);
const hasMore = ref<boolean>(false);
const isLoading = ref<boolean>(false);
const nextPage = ref<number>(1);

// Define on mounted
onMounted(() => {
	if (objectStore.is_loaded) {
		loadData();
	}
});

// Define watch
watch(
	() => objectStore.is_loaded,
	async (new_value) => {
		// If object data is now loaded - fetch data
		if (new_value) {
			await loadData();
		}
	}
)

// Define functions
function actionLabel(action: string): string {
	// Unknown actions (e.g. added by a newer backend) fall back to the raw value
	// (petite-vue-i18n hands back the key itself when it has no translation)
	const key = `audit_component.action_${action}`;
	const label = t(key);
	return label === key ? action : label;
}

function formatDate(value: string): string {
	return new Date(value).toLocaleString();
}

function formatValue(value: unknown): string {
	if (value === null || value === undefined || value === "") {
		return t("audit_component.empty_value");
	}
	return typeof value === "object" ? JSON.stringify(value) : String(value);
}

async function loadData(): Promise<void> {
	isLoading.value = true;

	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/audit/?page=${nextPage.value}`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			}
		}
	);

	switch (response.status) {
		case 200: {
			const data: AuditLogPageInterface = await response.json();

			auditList.value = auditList.value.concat(data.results);
			hasMore.value = data.next !== null;
			nextPage.value += 1;
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

	isLoading.value = false;
}
</script>

<template>
	<div class="audit">
		<p v-if="isLoading && auditList.length === 0">
			{{ t("audit_component.loading") }}
		</p>
		<p v-else-if="auditList.length === 0" class="empty">
			{{ t("audit_component.empty") }}
		</p>

		<ol v-else class="audit-list">
			<li v-for="entry in auditList" :key="entry.id" class="audit-entry">
				<div class="audit-header">
					<strong>{{ actionLabel(entry.action) }}</strong>
					<span v-if="entry.username">
						{{ t("audit_component.by", {username: entry.username}) }}
					</span>
					<time :datetime="entry.date_created">{{ formatDate(entry.date_created) }}</time>
				</div>

				<ul class="audit-changes" v-if="Object.keys(entry.changes).length > 0">
					<li v-for="(change, field) in entry.changes" :key="field">
						<span class="field">{{ field }}</span>:
						<span class="old">{{ formatValue(change.old) }}</span>
						&rarr;
						<span class="new">{{ formatValue(change.new) }}</span>
					</li>
				</ul>
			</li>
		</ol>

		<WlkButton class="compact"
		           v-if="hasMore"
		           v-on:click="loadData"
		>
			{{ t("audit_component.load_more") }}
		</WlkButton>
	</div>
</template>

<style scoped>
.audit {
	> .audit-list {
		list-style: none;
		margin: 0;
		padding: 0;

		> .audit-entry {
			padding: 0.5rem 0;
			border-bottom: 1px solid var(--wlk-border-color, currentColor);

			> .audit-header {
				display: flex;
				flex-wrap: wrap;
				gap: 0.5rem;
				align-items: baseline;

				> time {
					margin-left: auto;
					font-size: 0.875em;
				}
			}

			> .audit-changes {
				margin: 0.25rem 0 0;
				padding-left: 1rem;
				overflow-wrap: anywhere;

				.old {
					text-decoration: line-through;
				}
			}
		}
	}

	> .wlk-button {
		margin-top: 0.5rem;
	}
}
</style>

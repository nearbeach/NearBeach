<script setup lang="ts">
import {onMounted, ref, watch} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {WlkButton, WlkCard, WlkModal, WlkModalFooter, WlkModalHeader, WlkTextInput} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import type {SprintLinkInterface} from "@/utils/interfaces/SprintLinkInterface.ts";
import {X} from "@lucide/vue";

// Define i18n
const {t} = useI18n({
    messages: {
        en: {
            close_modal: "Cancel",
            create_sprint: "Create Sprint",
            description: "Control sprints connected to current object.",
            empty_sprint_links: "No sprint links connected to this object.",
            modal_end_date: "Sprint End Date",
            modal_sprint_title: "Sprint Title",
            modal_start_date: "Sprint Start Date",
            sprint_title: "Sprints",
        },
        ja: {
            close_modal: "キャンセル",
            create_sprint: "スプリントを作成する",
            description: "現在のオブジェクトに接続されたコントロールスプリント",
            empty_sprint_links: "このオブジェクトに接続されたスプリントリンクはありません。",
            modal_end_date: "スプリント終了日",
            modal_sprint_title: "スプリントタイトル",
            modal_start_date: "スプリント開始日",
            sprint_title: "スプリント",
        },
    }
})

// Define stores
const objectStore = useObjectStore();

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

// Define onMounted
onMounted(async () => {
    if (objectStore.is_loaded) {
        await loadData();
    }
});

// Define functions
function closeModal() {
    modalClass.value = "";
}

async function createSprint() {
    // TODO - ADD CODE
}

async function loadData() {
    const response = await fetch(
        `/api/v1/${objectStore.destination}/${objectStore.id}/sprint/`,
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        }
    )

    const data = await response.json();

    switch (response.status) {
        case 200:
            sprintData.value = data;
            break;
        default:
            errorMessage.value = data.error;
            break;
    }
}

function openModal() {
    modalClass.value = "open";
}
</script>

<template>
    <div class="sprint-links">
        <h3>{{ t("sprint_title") }}</h3>
        <p class="sub-text">{{ t("description") }}</p>
        <div class="empty-sprint-list"
             v-if="sprintData.length === 0"
        >
            {{ t("empty_sprint_links") }}
        </div>

        <div class="sprint-list"
             v-if="sprintData.length > 0"
        >
            <WlkCard v-for="(sprint, index) in sprintData">

            </WlkCard>

        </div>

        <WlkButton class="compact primary"
                   @click="openModal"
        >
            {{ t("create_sprint") }}
        </WlkButton>
    </div>

    <teleport to="body">
        <WlkModal :class="modalClass">
            <WlkModalHeader>
                <div class="modal-header-row">
                    <h3>{{ t("create_sprint") }}</h3>
                    <X :size="20"
                       :aria-label="t('close_modal')"
                       v-on:click="closeModal"
                    />
                </div>
            </WlkModalHeader>

            <WlkTextInput :label="t('modal_sprint_title')" v-model="sprintTitleModel"/>
            <div class="date-row">
<!--                <WlkDate :label="t('modal_start_date')" v-model="sprintStartDateModel" />-->
<!--                <WlkDate :label="t('modal_end_date')" v-model="sprintEndDateModel" />-->
            </div>

            <WlkModalFooter class="modal-footer-row">
                <WlkButton class="compact secondary"
                           v-on:click="closeModal"
                >{{ t("close_modal") }}
                </WlkButton>
                <WlkButton class="compact primary"
                           v-on:click="createSprint"
                >{{ t("create_sprint") }}
                </WlkButton>
            </WlkModalFooter>

        </WlkModal>
    </teleport>
</template>

<style scoped>
.sprint-links {
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
}
</style>
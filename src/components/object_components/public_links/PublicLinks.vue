<script setup lang="ts">
import {onMounted, ref, watch} from "vue";
import type {PublicLinkInterface} from "@/utils/interfaces/PublicLinkInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {WlkButton} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import PublicLinkRow from "@/components/object_components/public_links/public_link_row/PublicLinkRow.vue";

// Define i18n
const {t} = useI18n({
    messages: {
        en: {
            create_public_link: "Create Public Link",
            delete_public_link: "Delete Public Link",
            description: "Control public access to project",
            is_active: "Is Active",
            public_link: "Public Link",
        },
        ja: {
            create_public_link: "公開リンクを作成",
            delete_public_link: "公開リンクを削除",
            description: "プロジェクトへの公開アクセスを制御する",
            is_active: "有効です",
            public_link: "公開リンク",
        },
    }
})

// Define stores
const objectStore = useObjectStore();

// Define refs
const errorMessage = ref<string>("");
const publicLinks = ref<PublicLinkInterface[]>([]);

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
async function createPublicLink() {
    const response = await fetch(
        `/api/v1/${objectStore.destination}/${objectStore.id}/public_link/`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFTOKEN": getCsrfToken(),
            },
        },
    );

    // Get data
    const data = await response.json();

    switch (response.status) {
        case 201:
            publicLinks.value.push(data);
            break;
        default:
            errorMessage.value = data.error;
            break;
    }
}

async function deleteLink(data: {id: string}) {
    // Remove the link from the publicLinks list
    publicLinks.value = publicLinks.value.filter((link) => {
        return link.id !== data.id;
    });

    // Tell the backend to delete the link
    await fetch(
        `/api/v1/${objectStore.destination}/${objectStore.id}/public_link/${data.id}/`,
        {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFTOKEN": getCsrfToken(),
            },
        },
    ).catch((error) => {
        // TODO - handle error property
        console.error(error);
    });
}

async function loadData() {
    const response = await fetch(
        `/api/v1/${objectStore.destination}/${objectStore.id}/public_link/`,
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
            publicLinks.value = data;
            break;
        default:
            errorMessage.value = data.error;
            break;
    }
}

async function updateActive(data: {id: string, index: number}) {
    // Get copy of data
    let public_link_row = publicLinks.value[data.index];

    // Checks and balances
    if (public_link_row === undefined || public_link_row === null) {
        // Nothing to do
        // TODO - Place is error notifying user of issue
        return;
    }

    // Mutate the data
    public_link_row.is_active = !public_link_row.is_active;

    // Update the data
    publicLinks.value[data.index] = public_link_row;

    // Update the backend
    const body = {
        is_active: public_link_row.is_active,
    }

    await fetch(
        `/api/v1/${objectStore.destination}/${objectStore.id}/public_link/${data.id}/`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFTOKEN": getCsrfToken(),
            },
            body: JSON.stringify(body),
        }
    ).catch((error) => {
        // TODO - handle error property
        console.error(error);
    });
}
</script>

<template>
    <div class="public-links">
        <h3>{{ t("public_link") }}</h3>
        <p class="sub-text">{{ t("description") }}</p>

        <table v-if="publicLinks.length > 0">
            <thead>
                <tr>
                    <td style="width:calc(100% - 110px);">{{ t("public_link") }}</td>
                    <td style="width:90px;">{{ t("is_active") }}</td>
                    <td style="width:20px;"></td>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(link, index) in publicLinks"
                    :key="link.id"
                >
                    <PublicLinkRow :id="link.id"
                                   :is-active="link.is_active"
                                   :index="index"
                                   v-on:delete-link="deleteLink"
                                   v-on:update-active="updateActive"
                                   />
                </tr>
            </tbody>
        </table>

        <WlkButton class="compact primary"
                   @click="createPublicLink"
        >
            {{t("create_public_link")}}
        </WlkButton>
    </div>
</template>

<style scoped>
.public-links {
    > table {
        table-layout: fixed;
        width: 100%;
        display: table;

        > thead > tr {
            font-weight: bold;
            font-size: 1.25rem;
            border: none;

            > td {
                border: none;
            }
        }

        > tbody > tr {
            font-weight: lighter;
            font-size: 1rem;
            border: none;

            > td {
                border: none;
            }
        }

        > tbody > tr:nth-child(odd) {
            background-color: var(--bg-dark);
        }
    }
}

</style>
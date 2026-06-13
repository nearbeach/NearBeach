<script setup lang="ts">
import {ref} from "vue";
import {Folder, Link2, UploadCloudIcon, Upload} from "lucide-vue-next";
import {WlkDropDown, WlkModal, WlkModalHeader, WlkDropDownItem} from "whelk-ui";
import NewFolder from "@/components/object_components/document/create_and_filter/new_folder/NewFolder.vue";
import NewLink from "@/components/object_components/document/create_and_filter/new_link/NewLink.vue";
import UploadDocument
	from "@/components/object_components/document/create_and_filter/upload_document/UploadDocument.vue";
import {useI18n} from "petite-vue-i18n";
import {X} from "lucide-vue-next";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			"close_modal": "Click to close current modal",
			"new_folder": "Create a new folder",
			"new_link": "Create a new hyperlink",
			"upload": "Upload",
			"upload_document": "Upload a document",
		},
		ja: {
			"close_modal": "現在のモーダルを閉じるにはクリックしてください",
			"new_folder": "新しいフォルダーを作成する",
			"new_link": "新しいハイパーリンクを作成する",
			"upload": "アップロード",
			"upload_document": "ドキュメントをアップロードする",
		},
	}
});

// Define refs
const dropdownModel = ref<boolean>(false);
const headerString = ref<string>("");
const modalClass = ref<string>("");
const updateType = ref<string>("new_folder");

// Define functions
function closeModal() {
	modalClass.value = "";
}

function dropDownItemClicked(event: string) {
	// Close the dropdown
	dropdownModel.value = false;

	// Change the upload type
	updateType.value = event;

	// Header string
	headerString.value = t(event);

	// Show the modal
	modalClass.value = " open";
}
</script>

<template>
	<div class="document-create-and-filter">
		<WlkDropDown v-model="dropdownModel">
			<template v-slot:button>
				<Upload :size="12"/>
				{{t("upload")}}
			</template>
			<template v-slot:drop-down-items>
				<WlkDropDownItem v-on:click="dropDownItemClicked('new_folder')">
					<Folder :size="12"/>
					{{t("new_folder")}}
				</WlkDropDownItem>

				<WlkDropDownItem v-on:click="dropDownItemClicked('new_link')">
					<Link2 :size="12"/>
					{{t("new_link")}}
				</WlkDropDownItem>

				<WlkDropDownItem v-on:click="dropDownItemClicked('upload_document')">
					<UploadCloudIcon :size="12"/>
					{{t("upload_document")}}
				</WlkDropDownItem>
			</template>
		</WlkDropDown>
		<div class="filter">
			<input type="text" aria-label="Filter documents" placeholder="Filter documents..."/>
		</div>
	</div>

	<teleport to="body">
		<WlkModal :class="modalClass">
			<WlkModalHeader>
				<div class="modal-header-row">
					<h3>{{ headerString }}</h3>
					<X :size="20"
					   :aria-label="t('close_modal')"
					   v-on:click="closeModal"
					/>
				</div>
			</WlkModalHeader>
			<NewFolder
				v-if="updateType==='new_folder'"
				v-on:closeModal="closeModal"
			/>
			<NewLink
				v-if="updateType==='new_link'"
				v-on:closeModal="closeModal"
			/>
			<UploadDocument
				v-if="updateType==='upload_document'"
				v-on:closeModal="closeModal"
			/>
		</WlkModal>
	</teleport>
</template>

<style scoped>
.document-create-and-filter {
	display: flex;
	flex-direction: row;
	margin-top: 2rem;

	> .filter {
		flex: 1;

		> input {
			height: 1.75rem;
			font-size: 0.75rem;
			line-height: 1rem;
			padding: 0.1rem 0.5rem;
			border: solid;
			border-width: var(--border-width);
			border-color: var(--border-muted);
			border-radius: var(--border-radius);
			margin: 0 0 0 0.25rem;
			width: calc(100% - 1.5rem);

			@media (--small-screen) {
				margin: 0 0 0 1rem;
				width: calc(100% - 2rem);
			}
		}
	}
}

.modal-header-row {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
}
</style>
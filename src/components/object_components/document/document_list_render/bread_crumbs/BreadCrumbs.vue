<script setup lang="ts">
import {computed, type PropType} from "vue";
import type {FolderItemInterface} from "@/utils/interfaces/documents/FolderItemInterface.ts";
import {useI18n} from "petite-vue-i18n";
import type {BreadCrumbsArrayInterface} from "@/utils/interfaces/documents/BreadCrumbsArrayInterface.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			rootLabel: "Root",
		},
		ja: {
			rootLabel: "ルートディレクトリ",
		},
	}
})

// Define props
const props = defineProps({
	breadCrumbsArray: {
		type: Array as PropType<BreadCrumbsArrayInterface[]>,
		required: true,
	},
});

// Define emits
const emits = defineEmits(["goToRootFolder","updateFolderLocation"]);

// Define computed
const currentFolderLabel = computed(() => {
	// If folderArray length is 0 - return null string
	if (props.breadCrumbsArray?.length === 0) {
		return t("rootLabel");
	}

	// Get last array object and return the label
	return props.breadCrumbsArray[props.breadCrumbsArray.length - 1]?.description;
});

const getInbetweenFolders = computed(() => {
	if (props.breadCrumbsArray?.length <= 1) {
		// Nothing to return
		return [];
	}

	return props.breadCrumbsArray.slice(0, props.breadCrumbsArray?.length - 1);
});
</script>

<template>
	<div class="bread-crumbs">
		<a
			v-if="breadCrumbsArray.length > 0"
			type="button"
			class="root-button"
			v-on:click="emits('goToRootFolder')"
		>
			{{t("rootLabel")}}
		</a>
		<span class="middle-span">
			<a v-for="(folder, index) in getInbetweenFolders"
			   class="navigation-button"
			   type="button"
			   :key="folder.id"
			   v-on:click="emits('updateFolderLocation', { index })"
			>
				{{folder.description}}
			</a>
		</span>
		<span class="end-span">{{currentFolderLabel}}</span>
	</div>
</template>

<style scoped>
.bread-crumbs {
	display: flex;
	flex-direction: row;
	border-bottom: dashed;
	border-bottom-color: var(--border-muted);
	border-bottom-width: var(--border-width);
	padding: 1.5rem 0 0.5rem 0;
	font-weight: 100;
	font-family: "Roboto", sans-serif;

	> .root-button {
		text-decoration-color: var(--document-links);
		color: var(--document-links);

		&:after {
			content: "/";
		}
	}

	> .middle-span href="#"{
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		direction: rtl;

		> .navigation-button {
			text-decoration-color: var(--document-links);
			color: var(--document-links);

			&:after {
				content: "/";
			}

			&:last-child {
				&:after {
					content: "";
				}
			}
		}
	}

	> .end-span {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		max-width: 50%;
	}
}

</style>
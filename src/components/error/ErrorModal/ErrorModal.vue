<script setup lang="ts">
import {computed, ref, watch} from "vue";
import {useErrorStore} from "@/stores/error/error.ts";
import {WlkModalHeader, WlkModal, WlkModalFooter, WlkButton} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			"close_modal": "Click to close current modal",
			"title": "You have encountered an error",
		},
		jp: {
			"close_modal": "現在のモーダルを閉じるにはクリックしてください",
			"title": "エラーが発生しました",
		},
	}
});

// Define store
const errorStore = useErrorStore();

// Define ref
const disableButtons = ref<boolean>(true);

// Define computed
const modalClass = computed(() => {
	return errorStore.showErrorModal ? "wlk-modal open" : "wlk-modal";

});

// Define watches
watch(
	() => errorStore.showErrorModal,
	(new_value) => {
		// If true - disable button and set timeout
		if (new_value) {
			disableButtons.value = true;

			setTimeout(() => {
				disableButtons.value = false;
			}, 1000);
		}
	}
)
</script>

<template>
	<teleport to="body">
		<WlkModal :class="modalClass">
			<WlkModalHeader>
				<div class="modal-header-row">
					<h3>{{ t("title") }}</h3>
				</div>
			</WlkModalHeader>
			{{ errorStore.message }}
			<WlkModalFooter>
				<WlkButton
					class="info"
					v-on:click="errorStore.showErrorModal = false"
				>
					{{t("close_modal")}}
				</WlkButton>
			</WlkModalFooter>
		</WlkModal>
	</teleport>

</template>

<style scoped>

</style>
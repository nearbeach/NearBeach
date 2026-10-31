<script setup lang="ts">
import {computed} from "vue";
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

// Define computed
const modalClass = computed(() => {
	return errorStore.showErrorModal ? "wlk-modal open" : "wlk-modal";

});
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
					class="info compact"
					v-on:click="errorStore.showErrorModal = false"
				>
					{{t("close_modal")}}
				</WlkButton>
			</WlkModalFooter>
		</WlkModal>
	</teleport>
</template>

<style scoped>
.wlk-modal {
	> .wlk-modal-footer {
		padding-top: 0.75rem;
	}
}

</style>
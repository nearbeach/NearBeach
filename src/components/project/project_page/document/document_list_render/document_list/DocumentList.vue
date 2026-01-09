<script setup lang="ts">
import {Image, File, FileText, Link, Presentation, Trash} from "lucide-vue-next";
import type {PropType} from "vue";

// Define props
import type {DocumentItemInterface} from "@/utils/interfaces/DocumentItemInterface.ts";

defineProps({
	documentList: {
		type: Array as PropType<DocumentItemInterface[]>,
		required: true,
	},
});

// Define computed
function getIcon(type: string) {
	switch (type) {
		case "image":
			return Image;
		case "document":
			return FileText;
		case "link":
			return Link;
		case "powerpoint":
			return Presentation;
		default:
			return File;
	}
}

</script>

<template>
	<div class="document-list">
		<div
			class="document-item"
			v-for="item in documentList"
			:key="item.documentKey"
		>
			<div class="document-icon">
				<component :is="getIcon(item.type)" />
			</div>
			<div class="document-details">
				<p>
					<a href="javascript:void">{{ item.filename }}</a>
				</p>
				<p>Uploader: Socks Fluffybutt - on Jan 14th 2020</p>
			</div>
			<div class="document-delete">
				<Trash />
			</div>
		</div>
	</div>
</template>

<style scoped>
.document-list {
	display: flex;
	flex-direction: column;

	> .document-item {
		display: grid;
		grid-template-columns: [icon] 2rem [details] minmax(0, 1fr) [delete] 1rem;
		margin: 0 0 0.375rem 0;

		> .document-icon {
			grid-column: icon;

			> svg {
				flex: 1;
				width: 2rem;
				height: 2rem;
				stroke-width: 1px;
				color: var(--document-links);

				&:hover {
					fill: var(--document-links-hover);
				}
			}
		}

		> .document-details {
			padding-left: 0.25rem;
			grid-column: details;

			> p {
				margin: 0;
				font-size: 0.75rem;
				padding: 0;
				line-height: 1rem;
				font-family: "Roboto", sans-serif;
				text-overflow: ellipsis;
				overflow: hidden;
				white-space: nowrap;

				> a {
					text-decoration: none;
				}

				&:last-child {
					font-weight: 100;
				}
			}
		}

		> .document-delete {
			grid-column: delete;

			> svg {
				opacity: 0;
				transition: opacity 0.5s;
				flex: 1;
				width: 1rem;
				height: 1rem;
				stroke-width: 1px;
				color: var(--danger);

				&:hover {
					color: var(--danger-hover);
				}
			}
		}

		&:hover {
			> .document-delete {
				> svg {
					transition: opacity 1s;
					opacity: 1;
				}
			}
		}
	}
}
</style>
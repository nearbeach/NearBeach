<script setup lang="ts">
import {Image, File, FileText, Link, Presentation, Trash} from "lucide-vue-next";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";

// Define store
const documentationStore = useDocumentationStore();

// Define computed
function getIcon(description: string | null, urlLocation: string | null) {
	if (urlLocation !== null && urlLocation !== undefined && urlLocation !== "") {
		// Links do not have a urlLocation
		return Link;
	}

	// Make sure we have a file type at end of description
	const splitDescription : string[] | undefined = description?.split(".");
	if (splitDescription === undefined || splitDescription?.length === 0) {
		return File;
	}

	// Get the type and return the appropriate logo
	const type = splitDescription[splitDescription?.length -1];
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
			v-for="item in documentationStore.getDocuments"
			:key="item.key"
		>
			<div class="document-icon">
				<component :is="getIcon(item.description, item.url_location)" />
			</div>
			<div class="document-details">
				<p>
					<a
						target="_blank"
						:href="`/private/${item.key}/`"
					>
						{{ item.description }}
					</a>
				</p>
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
		grid-template-columns: [icon] 1.5rem [details] minmax(0, 1fr) [delete] 1rem;
		margin: 0 0 0.375rem 0;

		> .document-icon {
			grid-column: icon;

			> svg {
				flex: 1;
				width: 1.5rem;
				height: 1.5rem;
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
			display: flex;
			align-items: center;

			> p {
				margin: 0;
				font-size: 0.75rem;
				padding: 0;
				line-height: 1.5rem;
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
				color: hotpink;

				&:hover {
					color: cornflowerblue;
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
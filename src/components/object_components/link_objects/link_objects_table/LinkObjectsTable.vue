<script setup lang="ts">
import RelationshipLink from "@/components/object_components/link_objects/relationship_link/RelationshipLink.vue";
import {TrashIcon} from "lucide-vue-next";
import type {ObjectLinkInterface} from "@/utils/interfaces/ObjectLinkInterface.ts";
import {type PropType} from "vue";
import {useI18n} from "petite-vue-i18n";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			create: "Please wait - creating object link",
			error: "Error",
		},
		ja: {
			create: "しばらくお待ちください - オブジェクトリンクを作成しています",
			error: "エラー",
		}
	}
});

// Define props
defineProps({
	errorText: {
		type: String,
		default: "",
	},
	objectLinkList: {
		type: Array as PropType<ObjectLinkInterface[]>,
		required: true,
	},
	showCreate: {
		type: Boolean,
		default: false,
	},
});

// Define emits
const emit = defineEmits(["deleteObjectLink", "updateRelationship"])

// Define functions
async function deleteObjectLink(object_assignment_id: number, index: number) {
	emit("deleteObjectLink", {
		"object_assignment_id": object_assignment_id,
		"index": index,
	})
}

function updateRelationship(data: { index: number, link_relationship: string }) {
	emit("updateRelationship", {data})
}
</script>

<template>
	<div class="link-objects-table">
		<div
			v-for="(relationship, index) of objectLinkList"
			class="link-object"
		>
			<div class="link-object-info">
				<p>{{ relationship.object_status }}</p>
				<h4>{{ relationship.object_title }}</h4>
			</div>
			<div class="link-object-status">
				<RelationshipLink
					:index="index"
					:object-assignment-id="relationship.object_assignment_id"
					:object-id="relationship.object_id"
					:object-type="relationship.object_type"
					:relationship="relationship.link_relationship"
					:reverse-relationship="relationship.reverse_relation"
					v-on:update-relationship="updateRelationship"
				/>
			</div>
			<div class="link-object-delete">
				<TrashIcon
					width="20"
					height="20"
					v-on:click="deleteObjectLink(relationship.object_assignment_id, index)"
				/>
			</div>
		</div>

		<div
			v-if="showCreate"
			class="link-object"
		>
			<div class="link-create">
				<p>{{ t("create")}}</p>
			</div>
		</div>

		<div
			v-if="errorText !== ''"
			class="link-object"
		>
			<div class="link-error">
				<h4>{{ t("error")}}</h4>
				{{ errorText }}
			</div>
		</div>
	</div>

</template>

<style scoped>
.link-objects-table {
	display: flex;
	flex-direction: column;
	margin-bottom: 2rem;

	> .link-object {
		display: flex;
		flex-direction: column;
		border: 1px black dashed;
		padding: 1rem 0.5rem 0 0.5rem;
		margin-bottom: 2rem;

		@media (--medium-screen) {
			flex-direction: row;
			padding-right: 3rem;
		}

		@media (--large-screen) {
			padding-right: 0.5rem;
			margin-bottom: 0;
			border-top: none;

			&:first-child {
				border: 1px black dashed;
			}

			&:last-child data{
				margin-bottom: 2rem;
			}
		}

		> .link-object-info {
			width: 100%;

			h4 {
				font-size: 1.2rem;
				font-weight: bold;
				margin-bottom: 0.5rem;
			}

			> p {
				margin: 0;
				font-size: 0.875rem;
				font-weight: lighter;
			}
		}

		> .link-object-status {
			width: 100%;

			@media (--medium-screen) {
				width: 30%;
				max-width: 12rem;
			}
		}

		> .link-object-delete {
			position: absolute;
			left: 100%;
			transform: translate(-2.5rem, -0.25rem);

			& :hover {
				background-color: var(--secondary-hover);
			}

			@media (--medium-screen) {
				transform: translate(-3.75rem, -0.25rem);
			}

			@media (--large-screen) {
				position: inherit;
				transform: translate(0.5rem, -1rem);
				padding: 0.5rem;
			}

			> svg {
				width: 18px;
				height: 18px;
			}
		}

		> .link-create {
			width: 100%;
			text-align: center;
			font-weight: lighter;
			padding-bottom: 1rem;

			> p {
				margin: 0;
				font-size: 0.75rem;
			}
		}

		> .link-error {}
	}
}
</style>
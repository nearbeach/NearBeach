<script setup lang="ts">
import {useSearchStore} from "@/stores/search/search.ts";

// Define stores
const searchStore = useSearchStore();

</script>

<template>
	<div class="search-organisation-results">
		<div class="organisation-item"
		     v-for="organisation in searchStore.searchResults"
		     :key="organisation.id"
		>
			<RouterLink :to="`/organisation/${organisation.id}/`">
				<h3 aria-label="Organisation Name">
					{{ organisation.name }}
				</h3>
			</RouterLink>
			<p aria-label="Organisation contact details">
				<strong>Website:</strong> {{ organisation.website }}<br/>
				<strong>Email:</strong> {{ organisation.email }}
			</p>

		</div>

	</div>
</template>

<style scoped>
.search-organisation-results {
	display: flex;
	flex-direction: column;
	width: 100vw;
	overflow: clip;

	@media (--medium-screen) {
		margin: 0.5rem;
		width: auto;
		flex-direction: row;
		flex-wrap: wrap;
		justify-content: space-between;
	}

	.organisation-item {
		padding: 0.75rem 0.5rem;
		margin: 0.5rem 0;
		border-radius: var(--wlk-border-radius);
		background-color: var(--wlk-neutral-colour-11);
		color: var(--wlk-text);
		border-color: var(--wlk-neutral-colour-8);
		border-width: var(--wlk-border-width);
		border-style: var(--wlk-border-style);

		&:hover {
			background-color: var(--wlk-neutral-colour-10);
		}

		> a {
			text-decoration-style: dashed;

			> h3 {
				white-space: nowrap;
				overflow: hidden;
				text-overflow: ellipsis;
				font-size: 1.25rem;
				color: var(--document-links);
			}
		}

		> p {
			font-size: 0.75rem;
			line-height: 1rem;
			margin-top: 0.25rem;
			font-weight: lighter;
		}

		@media (--medium-screen) {
			width: 48%;
		}
	}
}

</style>
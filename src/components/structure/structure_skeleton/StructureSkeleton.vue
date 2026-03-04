<script setup lang="ts">

</script>

<template>
	<div class="structure-skeleton">
		<header role="banner"/>

		<div class="skeleton-card">
			<div class="skeleton-header"/>
			<div class="skeleton-line extra-margin"/>
			<div class="skeleton-line"/>
			<div class="skeleton-line"/>
			<div class="skeleton-line"/>
		</div>
	</div>
</template>

<style scoped>
.structure-skeleton {
	background-color: var(--bg-dark);
	display: flex;
	flex-direction: row;
	width: 100vw;
	height: 100vh;

	> header {
		background-color: white;
		position: fixed;
		top: 0;
		width: 100vw;
		height: 60px;

		@media (--small-screen) {
			height: 45px;
		}
	}

	> .skeleton-card {
		width: 100%;
		height: 500px;
		margin: 5rem 0.5rem;
		border-radius: var(--border-radius);
		background-color: var(--bg-light);

		> .skeleton-header {
			animation: skeleton-loading-header 1s linear infinite alternate;
			width: 80%;
			padding: 1rem 0;
			background-color: var(--text-red);
			margin: 1rem;
		}

		> .skeleton-line {
			animation: skeleton-loading-line 1s linear infinite alternate;
			width: calc(100% - 2rem);
			padding: 0.5rem 0;
			background-color: var(--text-muted);
			margin: 1rem;

			&.extra-margin {
				margin-top: 3rem;
			}
		}

		@media (--x-large-screen) {
			max-width: 1200px;
			margin: 5rem auto;
		}
	}
}

@keyframes skeleton-loading-header {
    0% {
        background-color: var(--loading-red-1);
    }
    100% {
        background-color: var(--loading-red-2);
    }
}

@keyframes skeleton-loading-line {
	0% {
		background-color: var(--loading-dark-1);
	}
	100% {
		background-color: var(--loading-dark-2);
	}
}
</style>
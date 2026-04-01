<script setup lang="ts">

</script>

<template>
	<div class="bread-crumbs">
		<a href="#" type="button" class="root-button">Root</a>
		<span class="middle-span">
			<a href="javascript:void(0)" type="button" class="navigation-button">Designs</a>
			<a href="javascript:void(0)" type="button" class="navigation-button">Project Design</a>
			<a href="javascript:void(0)" type="button" class="navigation-button">Wireframe</a>
		</span>
		<span class="end-span">/Final Draft of wireframe design</span>
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

	> .middle-span {
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
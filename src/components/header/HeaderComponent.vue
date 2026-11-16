<script lang="ts" setup>
import {useNavStore} from '@/stores/nav/nav.ts';
import {Menu} from '@lucide/vue'
import {computed} from 'vue';

// Stores
const navStore = useNavStore();

// Computed
const toggleMenuText = computed(() => {
	return navStore.isNavOpen
		? 'Close Navigation Menu'
		: 'Open Navigation Menu';
});

// Methods
function openNav(): void {
	navStore.toggleNav();
}
</script>

<template>
	<header role="banner">
		<div class="header--show-menu">
			<button :aria-label="toggleMenuText"
			        v-on:click="openNav"
			>
				<Menu :size="36" aria-hidden="true"/>
			</button>
		</div>
		<div class="nearbeach-logo" aria-hidden="true"></div>
		<div class="header--profile">
		</div>
	</header>
</template>

<style scoped>
header {
	background-color: white;
	position: sticky;
	top: 0;
	width: calc(100vw - 20px);
	height: calc(60px - 8px);
	display: flex;
	flex-direction: row;
	padding: 4px 10px;
	justify-content: space-between;

	@media (--small-screen) {
		height: calc(45px - 8px);
	}

	> .header--show-menu {
		display: flex;
		justify-content: center;
		align-items: center;

		> button {
			background: none;
			border: none;
			padding: 0.5rem;

			> svg {
				@media (--small-screen) {
					width: 16px;
					height: 16px;
				}
			}
		}
	}

	> .nearbeach-logo {
		background-image: url('../../assets/nearbeach_logo.svg');
		background-repeat: no-repeat;
		background-position: center;
		width: 100%;
		height: 36px;
		margin: auto;

		@media (--small-screen) {
			height: 27px;
			margin-top: 7px;
		}
	}

	> .header--profile {
		width: 50px;
		min-width: 50px;
		height: 50px;
		min-height: 50px;
		border-radius: 50%;
		object-fit: cover;
		background-color: #0a3069;

		@media (--small-screen) {
			width: 32px;
			min-width: 32px;
			height: 32px;
			min-height: 32px;
		}
	}
}
</style>

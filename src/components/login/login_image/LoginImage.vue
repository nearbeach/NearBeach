<script setup lang="ts">
import {onMounted, ref} from 'vue';

// Define refs
const imageSrc = ref('');

// On Mounted
onMounted(() => {

	// Fetch static from #loginApp
	const imageNumber = Math.floor(Math.random() * 5) + 1;
	
	imageSrc.value = `https://demo.nearbeach.app/static/NearBeach/images/NearBeach_Background_00${imageNumber}.webp`;
})
</script>

<template>
	<div class="login-image">
		<img :src="imageSrc"  alt="Login Image"/>
	</div>
</template>

<style scoped>
.login-image {
	display: none;
	max-width: 50vw;

	@media (--medium-screen) {
		display: flex;
	}

	> img {
		margin: 1rem 0 1rem 1rem;
		width: calc(50vw - 1rem);
		height: calc(100% - 2rem);
		border-radius: var(--border-radius);
		object-fit: cover;
		object-position: center;
	}
}
</style>
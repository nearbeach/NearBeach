<script setup lang="ts">
import {ref, watch} from 'vue';
import {useRoute} from 'vue-router';

const route = useRoute();
const backToTop = ref();

// Define watch
watch(
	() => route.path,
	() => {
		backToTop.value.focus();
	}
);

// Define functions
function skipToMain() {
	const main = document.getElementById('main')
	if (!main) return

	// Make it programmatically focusable if it isn't already
	if (!main.hasAttribute('tabindex')) {
		main.setAttribute('tabindex', '-1')
	}

	main.focus()
	main.scrollIntoView()

	// Optional: remove tabindex after blur so it's not in the normal tab order
	main.addEventListener('blur', () => {
		main.removeAttribute('tabindex')
	}, {once: true})
}
</script>

<template>
	<span ref="backToTop" tabindex="-1"/>
	<ul class="skip-links">
		<li>
			<!--suppress HtmlUnknownAnchorTarget -->
			<a href="#main"
			   ref="skipLink"
			   class="skip-link"
			   @click.prevent="skipToMain"
			>Skip to main content</a
			>
		</li>
	</ul>
</template>

<style scoped>
.skip-links {
	list-style: none;
	margin: 0;
}

.skip-link {
	white-space: nowrap;
	margin: 1em auto 1em -72px;
	top: 0;
	position: fixed;
	left: 50%;
	opacity: 0;
}

.skip-link:focus {
	opacity: 1;
	background-color: white;
	padding: 0.5em;
	border: 1px solid black;
}
</style>

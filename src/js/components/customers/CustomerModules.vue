<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<!-- The MENU Items -->
				<ul
					id="misc_module_tabs"
					class="nav nav-tabs"
					role="tablist"
				>
					<!-- Associated Projects & Tasks -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							id="associated-objects-tab"
							class="nav-link active"
							data-bs-toggle="tab"
							data-bs-target="#associated-objects"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Associated Objects
						</button>
					</li>

					<!-- ADMIN -->
					<li
						v-if="userLevel === 4"
						class="nav-item"
						role="presentation"
					>
						<button
							id="admin-tab"
							class="nav-link"
							data-bs-toggle="tab"
							data-bs-target="#admin"
							type="button"
							role="tab"
							aria-controls="home"
							aria-select="false"
						>
							Admin
						</button>
					</li>
				</ul>
				<hr/>

				<!-- The Modules -->
				<div
					id="misc_module_content"
					class="tab-content"
				>
					<div
						id="associated-objects"
						class="tab-pane fade active show"
						role="tabpanel"
						aria-labelledby="profile-tab"
					>
						<associated-objects
						></associated-objects>
					</div>

					<div
						v-if="userLevel === 4"
						id="admin"
						class="tab-pane fade bg-danger"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
						<delete-object></delete-object>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import AssociatedObjects from "Modules/sub_modules/AssociatedObjects.vue";
import { mapGetters } from "vuex";

//Composable
import {useNBTheme} from "Composables/theme/useNBTheme";
import DeleteObject from "Modules/sub_modules/DeleteObject.vue";

export default {
	name: "CustomerModule",
	components: {
		DeleteObject,
		AssociatedObjects,
	},
	computed: {
		...mapGetters({
			theme: "getTheme",
			userLevel: "getUserLevel",
		}),
	},
	methods: {useNBTheme},
};
</script>



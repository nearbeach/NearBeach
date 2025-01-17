<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<!-- The MENU Items -->
				<ul
					class="nav nav-tabs"
					id="misc_module_tabs"
					role="tablist"
				>
					<!-- Associated Projects & Tasks -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link active"
							id="associated-objects-tab"
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
						class="nav-item"
						role="presentation"
						v-if="userLevel === 4"
					>
						<button
							class="nav-link"
							id="admin-tab"
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
					class="tab-content"
					id="misc_module_content"
					v-if="userLevel === 4"
				>
					<div
						class="tab-pane fade active show"
						id="associated-objects"
						role="tabpanel"
						aria-labelledby="profile-tab"
					>
						<associated-objects
						></associated-objects>
					</div>

					<div
						class="tab-pane fade bg-danger"
						id="admin"
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
import AssociatedObjects from "../modules/sub_modules/AssociatedObjects.vue";
import { mapGetters } from "vuex";

//Composable
import {useNBTheme} from "../../composables/theme/useNBTheme";
import DeleteObject from "../modules/sub_modules/DeleteObject.vue";

export default {
	name: "CustomerModule",
	methods: {useNBTheme},
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
};
</script>



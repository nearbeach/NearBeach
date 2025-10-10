<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<ul
					id="misc_module_tabs"
					class="nav nav-tabs"
					role="tablist"
				>
					<!-- CHANGE TASK LINKS -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							id="change-task-links-tab"
							class="nav-link active"
							data-bs-toggle="tab"
							data-bs-target="#change_task_links"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Change Task Links
						</button>
					</li>

					<!-- DESCRIPTION -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							id="description-tab"
							class="nav-link"
							data-bs-toggle="tab"
							data-bs-target="#description"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Description
						</button>
					</li>

					<!-- MISC -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							id="misc-tab"
							class="nav-link"
							data-bs-toggle="tab"
							data-bs-target="#misc"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Misc
						</button>
					</li>
				</ul>
				<hr/>

				<div
					id="misc_module_content"
					class="tab-content"
				>
					<div
						id="change_task_links"
						class="tab-pane fade active show"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
<!--						<change-task-link-list-vue></change-task-link-list-vue>-->
						<change-task-link-list></change-task-link-list>
					</div>
					<div
						id="description"
						class="tab-pane fade"
						role="tabpanel"
						aria-labelledby="home-tab"
					>
						<change-task-description></change-task-description>
					</div>

					<div
						id="misc"
						class="tab-pane fade"
						role="tabpanel"
						aria-labelledby="home-tab"
					>
						<change-task-misc></change-task-misc>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//Import components
import ChangeTaskDescription from "./modules/ChangeTaskDescription.vue";
import ChangeTaskLinkList from "./modules/ChangeTaskLinkList.vue";
import ChangeTaskMisc from "./modules/ChangeTaskMisc.vue"

//Naive UI
import { NConfigProvider } from "naive-ui";

//Composables
import {useNBTheme} from "Composables/theme/useNBTheme";

export default {
	name: "ChangeTaskModules",
	components: {
		ChangeTaskDescription,
		ChangeTaskLinkList,
		ChangeTaskMisc,
    	NConfigProvider,
	},
	props: {
		theme: {
			type: String,
			default: "light",
		}
	},
	beforeMount() {
		this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	methods: {useNBTheme}
};
</script>



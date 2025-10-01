<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<ul
					class="nav nav-tabs"
					id="misc_module_tabs"
					role="tablist"
				>
					<!-- CHANGE TASK LINKS -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link active"
							id="change-task-links-tab"
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
							class="nav-link"
							id="description-tab"
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
							class="nav-link"
							id="misc-tab"
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
					class="tab-content"
					id="misc_module_content"
				>
					<div
						class="tab-pane fade active show"
						id="change_task_links"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
<!--						<change-task-link-list-vue></change-task-link-list-vue>-->
						<change-task-link-list></change-task-link-list>
					</div>
					<div
						class="tab-pane fade"
						id="description"
						role="tabpanel"
						aria-labelledby="home-tab"
					>
						<change-task-description></change-task-description>
					</div>

					<div
						class="tab-pane fade"
						id="misc"
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
import {useNBTheme} from "../../composables/theme/useNBTheme";

export default {
	name: "ChangeTaskModules",
	methods: {useNBTheme},
	props: {
		theme: {
			type: String,
			default: "light",
		}
	},
	components: {
		ChangeTaskDescription,
		ChangeTaskLinkList,
		ChangeTaskMisc,
    	NConfigProvider,
	},
	beforeMount() {
		this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	}
};
</script>



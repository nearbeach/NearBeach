<template>
	<n-config-provider :theme="getTheme(theme)">
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
						<change-task-link-list-vue></change-task-link-list-vue>
					</div>
					<div
						class="tab-pane fade"
						id="description"
						role="tabpanel"
						aria-labelledby="home-tab"
					>
						<change-task-desctiption></change-task-desctiption>
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
import ChangeTaskDesctiption from "./modules/ChangeTaskDescription.vue";
import ChangeTaskLinkListVue from "./modules/ChangeTaskLinkList.vue";
import ChangeTaskMisc from "./modules/ChangeTaskMisc.vue"
import getThemeMixin from "../../mixins/getThemeMixin";

export default {
	name: "ChangeTaskModules",
	props: {
		theme: {
			type: String,
			default: "",
		}
	},
	mixins: [getThemeMixin],
	components: {
		ChangeTaskDesctiption,
		ChangeTaskLinkListVue,
		ChangeTaskMisc,
	},
};
</script>

<style scoped></style>

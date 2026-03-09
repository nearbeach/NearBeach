<script setup lang="ts">
import NavMenuItem from '@/components/nav/nav_menu/nav_menu_item/NavMenuItem.vue';
import {usePermissionStore} from "@/stores/permissions/permission.ts";
import {
	LayoutDashboard,
	SquareKanban,
	ClipboardList,
	FolderOpenIcon,
	ListTodo,
	ReplaceAll,
} from 'lucide-vue-next';
import {useI18n} from "petite-vue-i18n";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			dashboard_title: "Dashboard",
			dashboard_aria_label: "Go to dashboard",
			kanban_board_title: "Kanban Board",
			kanban_board_aria_label: "Search for kanban board",
			requirement_title: "Requirement",
			requirement_aria_label: "Search for requirement",
			project_title: "Project",
			project_aria_label: "Search for project",
			task_title: "Task",
			task_aria_label: "Search for task",
			request_for_change_title: "Request for change",
			request_for_change_aria_label: "Search for Request for Change",
		},
		ja: {
			dashboard_title: "ダッシュボード",
			dashboard_aria_label: "ダッシュボードへ移動",
			kanban_board_title: "カンバンボード",
			kanban_board_aria_label: "カンバンボードを検索",
			requirement_title: "要件",
			requirement_aria_label: "要件を検索する",
			project_title: "プロジェクト",
			project_aria_label: "プロジェクトを検索",
			task_title: "タスク",
			task_aria_label: "タスクを検索",
			request_for_change_title: "変更要求",
			request_for_change_aria_label: "変更要求を検索",
		},
	}
})

// Define store
const permissionStore = usePermissionStore();

// Define Functions
function canUserCreate(object: string) {
	// Get potential value
	let item_results: number | string = permissionStore.maximumPermissions[
		object as keyof typeof permissionStore.maximumPermissions
		];

	// Check value is a number
	if (typeof (item_results) !== "number") {
		// Not a number - return empty value
		return "";
	}

	return item_results >= 3 ? `/${object}/new` : "";
}
</script>

<template>
	<NavMenuItem
		destination="dashboard"
		route-address="/"
		route-address-new=""
		:override-aria-label="t('dashboard_aria_label')"
		:title="t('dashboard_title')"
	>
		<component :is="LayoutDashboard" :size="14"/>
	</NavMenuItem>

	<NavMenuItem
		v-if="permissionStore.maximumPermissions.kanban_board > 0"
		destination="kanban_board"
		route-address="/kanban_board"
		:route-address-new="canUserCreate('kanban_board')"
		:override-aria-label="t('kanban_board_aria_label')"
		:title="t('kanban_board_title')"
	>
		<component :is="SquareKanban" :size="14"/>
	</NavMenuItem>

	<NavMenuItem
		v-if="permissionStore.maximumPermissions.requirement > 0"
		destination="requirement"
		route-address="/requirement"
		:route-address-new="canUserCreate('requirement')"
		:override-aria-label="t('requirement_aria_label')"
		:title="t('requirement_title')"
	>
		<component :is="ClipboardList" :size="14"/>
	</NavMenuItem>

	<NavMenuItem
		v-if="permissionStore.maximumPermissions.project > 0"
		destination="project"
		route-address="/project"
		:route-address-new="canUserCreate('project')"
		:override-aria-label="t('project_aria_label')"
		:title="t('project_title')"
	>
		<component :is="FolderOpenIcon" :size="14"/>
	</NavMenuItem>

	<NavMenuItem
		v-if="permissionStore.maximumPermissions.task > 0"
		destination="task"
		route-address="/task"
		:route-address-new="canUserCreate('task')"
		:override-aria-label="t('task_aria_label')"
		:title="t('task_title')"
	>
		<component :is="ListTodo" :size="14"/>
	</NavMenuItem>

	<NavMenuItem
		v-if="permissionStore.maximumPermissions.request_for_change > 0"
		destination="request_for_change"
		route-address="/request_for_change"
		:route-address-new="canUserCreate('request_for_change')"
		:override-aria-label="t('request_for_change_aria_label')"
		:title="t('request_for_change_title')"
	>
		<component :is="ReplaceAll" :size="14"/>
	</NavMenuItem>
</template>

<style scoped>
.nav-bar--menu--icon {
	> svg {
		width: 20px;
		height: 20px;

		@media (--small-screen) {
			width: 14px;
			height: 14px;
		}
	}
}
</style>

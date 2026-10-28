import {beforeEach, describe, expect, test} from "vitest";
import {flushPromises, mount} from "@vue/test-utils";
import {createPinia, setActivePinia} from "pinia";
import {createMemoryHistory, createRouter} from "vue-router";
import {defineComponent, h} from "vue";
import {NavSettingMenu} from ".";
import {NavMenuItem} from "@/components/nav/nav_menu/nav_menu_item";
import {NavMenuLogout} from "@/components/nav/nav_menu/nav_menu_logout";
import {usePermissionStore} from "@/stores/permissions/permission.ts";
import i18n from "@/i18n.ts";

const page = defineComponent({render: () => h("div")});
const router = createRouter({
	history: createMemoryHistory(),
	routes: [{path: "/:catchAll(.*)*", component: page}],
});

async function mountMenu() {
	const wrapper = mount(NavSettingMenu, {global: {plugins: [router, i18n]}});
	await flushPromises();

	return wrapper;
}

describe("NavSettingMenu", () => {
	beforeEach(() => {
		setActivePinia(createPinia());
	});

	test("always offers the logout link", async () => {
		const wrapper = await mountMenu();

		expect(wrapper.findComponent(NavMenuLogout).exists()).toBe(true);
	});

	test("hides the settings link from people without administration permission", async () => {
		usePermissionStore().hasAdministrationPermission = false;

		const wrapper = await mountMenu();

		expect(wrapper.findComponent(NavMenuItem).exists()).toBe(false);
	});

	test("shows the settings link to people with administration permission", async () => {
		usePermissionStore().hasAdministrationPermission = true;

		const wrapper = await mountMenu();
		const item = wrapper.findComponent(NavMenuItem);

		expect(item.exists()).toBe(true);
		expect(item.props("destination")).toBe("settings");
		expect(item.props("routeAddress")).toBe("/settings");
		expect(item.props("title")).toBe("Settings");
	});

	test("the settings link follows the permission when it changes", async () => {
		const permissionStore = usePermissionStore();
		const wrapper = await mountMenu();
		expect(wrapper.findComponent(NavMenuItem).exists()).toBe(false);

		permissionStore.hasAdministrationPermission = true;
		await flushPromises();

		expect(wrapper.findComponent(NavMenuItem).exists()).toBe(true);
	});

	test("having permission on a single object type does not show settings", async () => {
		const permissionStore = usePermissionStore();
		permissionStore.permissionData = [
			{group_id: 1, group_name: "QA", project: 4} as never,
		];
		permissionStore.processPermissionData();

		const wrapper = await mountMenu();

		expect(wrapper.findComponent(NavMenuItem).exists()).toBe(false);
	});

	test("any one administration permission is enough to show settings", async () => {
		const permissionStore = usePermissionStore();
		permissionStore.permissionData = [
			{group_id: 1, group_name: "Admin", administration_create_user: 1} as never,
		];
		permissionStore.processPermissionData();

		const wrapper = await mountMenu();

		expect(wrapper.findComponent(NavMenuItem).exists()).toBe(true);
	});
});

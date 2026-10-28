import {describe, expect, test} from "vitest";
import {mount} from "@vue/test-utils";
import {NavMenuLogout} from ".";
import i18n from "@/i18n.ts";

function mountLogout() {
	return mount(NavMenuLogout, {global: {plugins: [i18n]}});
}

describe("NavMenuLogout", () => {
	test("is a list item holding one link", () => {
		const wrapper = mountLogout();

		expect(wrapper.element.tagName).toBe("LI");
		expect(wrapper.findAll("a")).toHaveLength(1);
	});

	test("the link goes to the logout address", () => {
		const link = mountLogout().find("a");

		expect(link.attributes("href")).toBe("/logout/");
	});

	test("shows the title and has a descriptive aria label", () => {
		const link = mountLogout().find("a");

		expect(link.text()).toBe("Logout");
		expect(link.attributes("aria-label")).toBe("Logout of NearBeach");
	});

	test("the icon is hidden from screen readers", () => {
		const icon = mountLogout().find(".nav-bar--menu--icon");

		expect(icon.exists()).toBe(true);
		expect(icon.attributes("aria-hidden")).toBe("true");
		expect(icon.find("svg").exists()).toBe(true);
	});
});

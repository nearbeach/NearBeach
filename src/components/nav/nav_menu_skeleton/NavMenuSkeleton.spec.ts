import {describe, test, expect} from "vitest";
import NavMenuSkeleton from "./NavMenuSkeleton.vue";

describe("NavMenuSkeleton", async () => {
	test("mounting component", async () => {
		// NavMenuSkeleton exists
		expect(NavMenuSkeleton).toBeTruthy();
	})
});
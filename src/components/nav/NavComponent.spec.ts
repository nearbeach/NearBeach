import { describe, expect, test } from "vitest";
import NavComponent from "./NavComponent.vue";

describe("NavComponent", () => {
  test("mounting component", async () => {
    // Header component exists
    expect(NavComponent).toBeTruthy();
  });
});

//TODO - test for v-show conditions
//TODO - test for different permissions, i.e. someone with no permissions to projects should not see projects

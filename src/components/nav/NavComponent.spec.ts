import { describe, expect, test } from "vitest";
import {NavComponent} from "./";

describe("NavComponent", () => {
  test("mounting component", () => {
    // Header component exists
    expect(NavComponent).toBeTruthy();
  });
});

//TODO - test for v-show conditions
//TODO - test for different permissions, i.e. someone with no permissions to projects should not see projects

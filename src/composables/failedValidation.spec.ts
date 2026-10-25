import { describe, expect, test } from "vitest";
import { failedValidation } from "@/composables/failedValidation.ts";

describe("failedValidation", () => {
    test("fails when there is no validation data", () => {
        expect(failedValidation(undefined as unknown as Record<string, boolean>)).toBe(true);
    });

    test("passes when every field is valid", () => {
        expect(failedValidation({ title: true, group: true })).toBe(false);
    });

    test("fails when any field is invalid", () => {
        expect(failedValidation({ title: true, group: false })).toBe(true);
    });

    test("passes when there are no fields to check", () => {
        expect(failedValidation({})).toBe(false);
    });
});

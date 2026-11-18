import { describe, expect, test } from "vitest";
import { formatObjectId } from "./formatObjectId.ts";

describe("formatObjectId", () => {
    test("Customer", () => {
        expect(formatObjectId("customer", 1)).toBe("cust-1");
        expect(formatObjectId("CUSTOMER", 1)).toBe("cust-1");
    });

    test("kanban_board", () => {
        expect(formatObjectId("kanban_board", 1)).toBe("kan-1");
        expect(formatObjectId("KANBAN_BOARD", 1)).toBe("kan-1");
    });

    test("kanban_card", () => {
        expect(formatObjectId("kanban_card", 1)).toBe("card-1");
        expect(formatObjectId("KANBAN_CARD", 1)).toBe("card-1");
    });

    test("request_for_change", () => {
        expect(formatObjectId("request_for_change", 1)).toBe("rfc-1");
        expect(formatObjectId("REQUEST_FOR_CHANGE", 1)).toBe("rfc-1");
    });

    test("requirement", () => {
        expect(formatObjectId("requirement", 1)).toBe("req-1");
        expect(formatObjectId("REQUIREMENT", 1)).toBe("req-1");
    });

    test("requirement_item", () => {
        expect(formatObjectId("requirement_item", 1)).toBe("item-1");
        expect(formatObjectId("REQUIREMENT_ITEM", 1)).toBe("item-1");
    });

    test("organisation", () => {
        expect(formatObjectId("organisation", 1)).toBe("org-1");
        expect(formatObjectId("ORGANISATION", 1)).toBe("org-1");
    });

    test("project", () => {
        expect(formatObjectId("project", 1)).toBe("pro-1");
        expect(formatObjectId("PROJECT", 1)).toBe("pro-1");
    });

    test("sprint", () => {
        expect(formatObjectId("sprint", 1)).toBe("spr-1");
        expect(formatObjectId("SPRINT", 1)).toBe("spr-1");
    });

    test("task", () => {
        expect(formatObjectId("task", 1)).toBe("task-1");
        expect(formatObjectId("TASK", 1)).toBe("task-1");
    });
});

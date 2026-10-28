import {describe, expect, test} from "vitest";
import {ObjectStateEnum} from "@/utils/enums/ObjectStateEnum.ts";
import {ObjectTitleCaseEnums} from "@/utils/enums/ObjectTitleCaseEnums.ts";
import {ObjectTypeEnums} from "@/utils/enums/ObjectTypeEnums.ts";

describe("ObjectTypeEnums", () => {
	test("every key matches its value (the value is what the api and urls use)", () => {
		for (const [key, value] of Object.entries(ObjectTypeEnums)) {
			expect(value).toBe(key);
		}
	});

	test("lists the object types the api knows about", () => {
		expect(Object.values(ObjectTypeEnums).sort()).toEqual([
			"customer",
			"kanban_board",
			"kanban_card",
			"organisation",
			"project",
			"request_for_change",
			"requirement",
			"requirement_item",
			"task",
		]);
	});
});

describe("ObjectTitleCaseEnums", () => {
	test("every object type has a title to show people", () => {
		for (const objectType of Object.values(ObjectTypeEnums)) {
			expect(ObjectTitleCaseEnums[objectType as keyof typeof ObjectTitleCaseEnums], objectType).toBeTruthy();
		}
	});

	test("titles are written for people, not as identifiers", () => {
		expect(ObjectTitleCaseEnums.request_for_change).toBe("Request For Change");
		expect(ObjectTitleCaseEnums.kanban_board).toBe("Kanban Board");
	});

	test("also has titles for groups and users, which are not objects", () => {
		expect(ObjectTitleCaseEnums.group).toBe("Group");
		expect(ObjectTitleCaseEnums.user).toBe("User");
	});
});

describe("ObjectStateEnum", () => {
	test("has a distinct value for every state", () => {
		const values = Object.values(ObjectStateEnum);

		expect(new Set(values).size).toBe(values.length);
	});

	test("values are upper case with underscores", () => {
		for (const value of Object.values(ObjectStateEnum)) {
			expect(value).toMatch(/^[A-Z_]+$/);
		}
	});

	test("includes the states the forms move through", () => {
		expect(ObjectStateEnum.NoAction).toBe("NO_ACTION");
		expect(ObjectStateEnum.Loading).toBe("LOADING");
		expect(ObjectStateEnum.Saving).toBe("SAVING");
		expect(ObjectStateEnum.Error).toBe("ERROR");
	});
});

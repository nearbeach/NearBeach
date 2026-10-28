import {describe, expect, test} from "vitest";
import shortObjectDictionary from "@/utils/dictionary/ShortObjectDictionary.ts";
import {ObjectTypeEnums} from "@/utils/enums/ObjectTypeEnums.ts";

describe("shortObjectDictionary", () => {
	test("every object type has a short name", () => {
		for (const objectType of Object.values(ObjectTypeEnums)) {
			expect(shortObjectDictionary[objectType], objectType).toBeTruthy();
		}
	});

	test("the short names are what the id tags show", () => {
		expect(shortObjectDictionary.project).toBe("Pro");
		expect(shortObjectDictionary.task).toBe("Task");
		expect(shortObjectDictionary.request_for_change).toBe("RFC");
		expect(shortObjectDictionary.requirement_item).toBe("Item");
	});

	test("no two object types share a short name", () => {
		const names = Object.values(shortObjectDictionary);

		expect(new Set(names).size).toBe(names.length);
	});

	test("an unknown object type has no short name", () => {
		expect(shortObjectDictionary["not_an_object"]).toBeUndefined();
	});
});

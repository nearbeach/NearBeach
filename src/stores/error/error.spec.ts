import {beforeEach, describe, expect, test} from "vitest";
import {createPinia, setActivePinia} from "pinia";
import {useErrorStore} from "@/stores/error/error.ts";

describe("Error store", () => {
	beforeEach(() => {
		setActivePinia(createPinia());
	});

	test("starts with no message and the modal closed", () => {
		const errorStore = useErrorStore();

		expect(errorStore.message).toBe("");
		expect(errorStore.showErrorModal).toBe(false);
	});

	test("setError takes the message from an Error", () => {
		const errorStore = useErrorStore();

		errorStore.setError(new Error("Response status: 500"));

		expect(errorStore.message).toBe("Response status: 500");
	});

	test("setError takes the message from a subclass of Error", () => {
		const errorStore = useErrorStore();

		errorStore.setError(new TypeError("Failed to fetch"));

		expect(errorStore.message).toBe("Failed to fetch");
	});

	test("setError turns anything else into text", () => {
		const errorStore = useErrorStore();

		const cases: Array<[unknown, string]> = [
			["plain text", "plain text"],
			[404, "404"],
			[null, "null"],
			[undefined, "undefined"],
			[{code: 1}, "[object Object]"],
		];
		for (const [input, expected] of cases) {
			errorStore.setError(input);

			expect(errorStore.message, String(input)).toBe(expected);
		}
	});

	test("a later error replaces the earlier one", () => {
		const errorStore = useErrorStore();

		errorStore.setError(new Error("first"));
		errorStore.setError(new Error("second"));

		expect(errorStore.message).toBe("second");
	});

	test("setError does not open the modal by itself", () => {
		const errorStore = useErrorStore();

		errorStore.setError(new Error("something"));

		expect(errorStore.showErrorModal).toBe(false);
	});
});

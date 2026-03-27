// stores/object.spec.ts
import {setActivePinia, createPinia} from "pinia";
import {describe, test, expect, beforeEach} from "vitest";
import {useObjectStore} from "@/stores/object/object.ts";

describe('Nav - check "toggleNav" action works', () => {
	beforeEach(() => {
		setActivePinia(createPinia());
	});

    test("Check defaults", async () => {
        const objectStore = useObjectStore();

        // Expects
        expect(objectStore.description).toBe("");
    });
});

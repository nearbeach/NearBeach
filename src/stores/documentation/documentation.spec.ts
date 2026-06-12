// stores/documentation.spec.ts
import {setActivePinia, createPinia} from "pinia";
import {describe, test, expect, beforeEach} from "vitest";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";

describe('Nav - todo', () => {
	beforeEach(() => {
		setActivePinia(createPinia());
	});

    test("Check defaults", async () => {
        const documentationStore = useDocumentationStore();

        // Expects
        expect("").toBe("");
    });
});

// stores/nav.spec.ts
import {setActivePinia, createPinia} from "pinia";
import {describe, test, expect, beforeEach} from "vitest";
import {useSearchStore} from "@/stores/search/search.ts";

describe("Search Stores - check getters", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
    });

    test("Check defaults are null", async () => {
        const search = useSearchStore();

        // Expects
        expect(search.previous).toBe(null);
        expect(search.next).toBe(null);
        expect(search.searchResults.length).toBe(0);
        expect(search.searchResults).toEqual([]);
    });

    test("Check defaults are null", async () => {
        const search = useSearchStore();

        // Set values
        search.previous = 0;
        search.next = 2;
        // search.searchResults = [{a: 1, b: 2}];
        // TODO - put types into search results and put test data here

        // Expects
        expect(search.previous).not.toBe(null);
        expect(search.next).not.toBe(null);
        expect(search.searchResults.length).not.toBe(0);
        // expect(search.searchResults).not.toEqual([]);
        expect(search.previous).toBe(0);
        expect(search.next).toBe(2);
        // expect(search.searchResults.length).toBe();
        // expect(search.searchResults).toEqual([]);
    });


})


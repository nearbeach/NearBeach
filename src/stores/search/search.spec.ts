// stores/search.spec.ts
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
        expect(search.getPrevious).toBe(null);
        expect(search.getNext).toBe(null);
        expect(search.getSearchResults.length).toBe(0);
        expect(search.getSearchResults).toEqual([]);
    });

    test("Check defaults are not null", async () => {
        const search = useSearchStore();
        const searchResults = [{"description":"<p>Project - QA Team</p>","id":2,"title":"Project - QA Team","end_date":"2023-03-01T05:00:00Z","start_date":"2023-02-14T22:00:00Z","organisation":{"id":1,"name":"NearBeach Incorporate","website":"https://nearbeach.org","email":"support@nearbeach.org","profile_picture_path":null,"customers":null},"priority":{"value":2,"label":"Normal"},"status":{"id":1,"status":"New","higher_order_status":{"value":"Backlog","label":"Backlog"}}},{"description":"<p>Project - Only Administration</p>","id":1,"title":"Project - Only Administration","end_date":"2023-03-01T05:00:00Z","start_date":"2023-02-14T22:00:00Z","organisation":{"id":1,"name":"NearBeach Incorporate","website":"https://nearbeach.org","email":"support@nearbeach.org","profile_picture_path":null,"customers":null},"priority":{"value":2,"label":"Normal"},"status":{"id":1,"status":"New","higher_order_status":{"value":"Backlog","label":"Backlog"}}}];

        // Set values
        search.previous = 0;
        search.next = 2;
        search.searchResults = searchResults;

        // Expects
        expect(search.getPrevious).not.toBe(null);
        expect(search.getNext).not.toBe(null);
        expect(search.getSearchResults.length).not.toBe(0);
        expect(search.getSearchResults).not.toEqual([]);
        expect(search.getPrevious).toBe(0);
        expect(search.getNext).toBe(2);
        expect(search.getSearchResults).toEqual(searchResults);
        expect(search.getSearchResults.length).toBe(2);
    });
})


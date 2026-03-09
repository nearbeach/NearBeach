// stores/search.ts
import { defineStore } from 'pinia'
import type {SearchResultsInterface} from "@/utils/interfaces/stores/SearchResultsInterface.ts";

export const useSearchStore = defineStore("search", {
    state: () => {
        return {
            previous: null as null | number,
            next: null as null | number,
            searchResults: [] as SearchResultsInterface[],
        }
    },
    getters: {
        getNext: (state) => state.next,
        getPrevious: (state) => state.previous,
        getSearchResults: (state) => state.searchResults,
    },
});

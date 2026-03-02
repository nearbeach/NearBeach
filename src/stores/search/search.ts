// stores/search.ts
import { defineStore } from 'pinia'

export const useSearchStore = defineStore("search", {
    state: () => {
        return {
            previous: null as null | number,
            next: null as null | number,
            searchResults: [],
        }
    },
    getters: {
        getNext: (state) => state.next,
        getPrevious: (state) => state.previous,
        getSearchResults: (state) => state.searchResults,
    },
});

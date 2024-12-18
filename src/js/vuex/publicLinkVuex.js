export const modulePublicLink = {
    state: () => ({
        publicLinkRemoveKey: "",
        publicLinkResults: [],
    }),
    mutations: {
        updatePublicLinkRemoveKey(state, payload) {
            state.publicLinkRemoveKey = payload.publicLinkRemoveKey;
        },
        updatePublicLinkResults(state, payload) {
            state.publicLinkResults = payload.publicLinkResults;
        },
    },
    actions: {
        removePublicLink: ({state, commit}, payload) => {
            const new_public_link_results = state.publicLinkResults.filter(row => {
                return row.public_link_id !== payload.public_link_id;
            });

            

            commit("updatePublicLinkResults", {
                publicLinkResults: new_public_link_results,
            });
        },
    },
    getters: {
        getPublicLinkRemoveKey: (state) => {
            return state.publicLinkRemoveKey;
        },
        getPublicLinkResults: (state) => {
            return state.publicLinkResults;
        },
    }
}
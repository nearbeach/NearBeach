export const moduleUrl = {
    state: () => ({
        rootUrl: "/",
        staticUrl: "/static/",
    }),
    mutations: {
        updateUrl(state, payload) {
            state.rootUrl = payload.rootUrl;
            state.staticUrl = payload.staticUrl;
        },
    },
    actions: {},
    getters: {
        getRootUrl: (state) => {
            return state.rootUrl;
        },
        getStaticUrl: (state) => {
            return state.staticUrl;
        },
    },
};

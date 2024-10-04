export const moduleConfirmDelete = {
    state: () => ({
        objectId: 0,
        objectType: "",
    }),
    mutations: {
        updateConfirmDelete(state, payload) {
            state.objectType = payload.objectType;
            state.objectId = payload.objectId;
        },
    },
    actions: {},
    getters: {
        getConfirmDeleteObjectId: (state) => {
            return state.objectId;
        },
        getConfirmDeleteObjectType: (state) => {
            return state.objectType;
        },
    }
}
export const moduleConfirmDelete = {
    state: () => ({
        objectId: 0,
        objectType: "",
        parentObjectId: 0,
        parentObjectType: "",
    }),
    mutations: {
        updateConfirmDelete(state, payload) {
            state.objectType = payload.objectType;
            state.objectId = payload.objectId;

            const poi = payload.parentObjectId;
            const pot = payload.parentObjectType;

            state.parentObjectId = poi === undefined || poi === null ? 0 : poi;
            state.parentObjectType = pot === undefined || pot === null ? "" : pot;
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
        getConfirmDeleteParentObjectId: (state) => {
            return state.parentObjectId;
        },
        getConfirmDeleteParentObjectType: (state) => {
            return state.parentObjectType;
        },
    }
}
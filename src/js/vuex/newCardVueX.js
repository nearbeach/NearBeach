export const moduleNewCard = {
    state: () => ({
        columnId: 0,
        levelId: 0,
        userCanSelectLocation: false,
    }),
    mutations: {
        updateNewCardLocation(state, payload) {
            state.columnId = payload.columnId;
            state.levelId = payload.levelId;
            state.userCanSelectLocation = payload.userCanSelectLocation;
        },
    },
    actions: {},
    getters: {
        getNewCardLocation: (state) => {
            return {
                columnId: state.columnId,
                levelId: state.levelId,
                userCanSelectLocation: state.userCanSelectLocation,
            }
        },
    },
};
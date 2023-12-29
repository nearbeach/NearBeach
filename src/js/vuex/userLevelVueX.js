export const moduleUserLevel = {
    state: () => ({
        userLevel: 0,
    }),
    mutations: {
        updateUserLevel(state, payload) {
            state.userLevel = payload.userLevel;
        },
    },
    action: {},
    getters: {
        getUserLevel: (state) => {
            return state.userLevel;
        },
    },
};

export const moduleGdpr = {
    state: () => ({
        validationData: {
            tab_0: false,
            tab_1: false,
            tab_2: false,
            tab_3: false,
        },
    }),
    mutations: {},
    actions: {

    },
    getters: {
        getValidationData: (state) => {
            return state.validationData;
        },
    },
}
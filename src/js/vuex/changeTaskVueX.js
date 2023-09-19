export const moduleChangeTask = {
    state: () => ({
        description: "",
        endDate: new Date(0),
        isDowntime: false,
        requiredBy: "",
        startDate: new Date(0),
    }),
    mutations: {
        updateChangeTask(state, payload) {
            state.description = payload.description;
            state.endDate = new Date(payload.endDate);
            state.isDowntime = payload.isDowntime;
            state.requiredBy = payload.requiredBy;
            state.startDate = new Date(payload.startDate);
        },
        updateChangeTaskDescription(state, payload) {
            state.description = payload.changeTaskDescription;
        },
        updateChangeTaskIsDowntime(state, payload) {
            state.isDowntime = payload.isDowntime;
        },
        updateChangeTaskRequiredBy(state, payload) {
            state.stakeholder = payload.requiredBy;
        },
    },
    actions: {},
    getters: {
        getChangeTaskDescription: (state) => {
            return state.description;
        },
        getChangeTaskEndDate: (state) => {
            return state.endDate;
        },
        getChangeTaskStartDate: (state) => {
            return state.startDate;
        },
        getChangeTaskIsDowntime: (state) => {
            return state.isDowntime;
        },
        getChangeTaskRequiredBy: (state) => {
            return state.requiredBy;
        },
    },
};

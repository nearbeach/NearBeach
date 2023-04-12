export const moduleChangeTask = {
	state: () => ({
        description: "",
        endDate: new Date(0),
        startDate: new Date(0),
	}),
	mutations: {
		updateChangeTask(state, payload) {
            state.description = payload.description;
            state.endDate = new Date(payload.endDate);
			state.startDate = new Date(payload.startDate);
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
	},
};

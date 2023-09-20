export const moduleArchiveCards = {
    state: () => ({
        archiveDestination: {
            column: "",
            level: "",
        },
    }),
    mutations: {
        updateArchiveDestination(state, payload) {
            state.archiveDestination.column = payload.column;
            state.archiveDestination.level = payload.level;
        },
    },
    actions: {},
    getters: {
        getArchiveDestination: (state) => {
            return state.archiveDestination;
        },
        getArchiveDestinationString: (state) => {
            //If there is an empty state - return undefined
            if (
                state.archiveDestination.column === "" ||
                state.archiveDestination.level === ""
            ) {
                return undefined;
            }

            //All is good
            return `${state.archiveDestination.column}|${state.archiveDestination.level}`;
        },
    },
};

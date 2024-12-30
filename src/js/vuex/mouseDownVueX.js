export const moduleMouseDown = {
    state: () => ({
        isMouseDown: false,
        mdClientXInitial: 0,
        mdIndex: 0,
        mdObjectId: 0,
        mdObjectType: "",
        mdParentObjectId: 0,
        mdParentObjectType: "",
        mdColumn: "",
        mdEndDateInitial: 0,
        mdHigherOrderStatus: "",
        mdStartDateInitial: 0,
        mdStatus: "",
        mdStatusId: 0,
        mdTitle: "",
    }),
    mutations: {
        updateMouseDown(state, payload) {
            //Loop through all the payload, and update the relevant state object
            for (const [key, value] of Object.entries(payload)) {
                state[key] = value;
            }
        },
    },
    actions: {},
    getters: {
        getIsMouseDown: (state) => {
            return state.isMouseDown;
        },
        getMdClientXInitial: (state) => {
            return state.mdClientXInitial;
        },
        getMdIndex: (state) => {
            return state.mdIndex;
        },
        getMdObjectId: (state) => {
            return state.mdObjectId;
        },
        getMdObjectType: (state) => {
            return state.mdObjectType;
        },
        getMdColumn: (state) => {
            return state.mdColumn;
        },
        getMdEndDateInitial: (state) => {
            return state.mdEndDateInitial;
        },
        getMdHigherOrderStatus: (state) => {
            return state.mdHigherOrderStatus;
        },
        getMdParentObjectId: (state) => {
            return state.mdParentObjectId;
        },
        getMdParentObjectType: (state) => {
            return state.mdParentObjectType;
        },
        getMdStartDateInitial: (state) => {
            return state.mdStartDateInitial;
        },
        getMdStatus: (state) => {
            return state.mdStatus;
        },
        getMdStatusId: (state) => {
            return state.mdStatusId;
        },
        getMdTitle: (state) => {
            return state.mdTitle;
        },
    },
}
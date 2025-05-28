export const moduleGdpr = {
    state: () => ({
        gdprObjectId: 0,
        gdprObjectType: "",
        userActionToRemove: {
            project: [],
            requirement: [],
            requirement_item: [],
            task: [],
        },
        validationData: {
            tab_0: false,
            tab_1: false,
            tab_2: false,
            tab_3: false,
        },
    }),
    mutations: {
        updateGdprObjectId(state, payload) {
            state.gdprObjectId = payload.gdprObjectId;
        },
        updateGdprObjectType(state, payload) {
            state.gdprObjectType = payload.gdprObject;
        },
        updateUserActionToRemove(state, payload) {
            state.userActionToRemove[payload.modelTarget] = payload.value;
        },
        updateValidationData(state, payload) {
            //Get a copy of the validation data
            let validation_data = state.validationData;

            //Mutate the copy
            validation_data[payload.tab_id] = payload.value;

            //Set
            state.validationData = validation_data;
        },
    },
    actions: {
        processGdprObjectId({commit}, payload) {
            commit({
                type: "updateGdprObjectId",
                gdprObjectId: payload.gdprObjectId,
            });

            // Get validation conditions
            const condition_1 = payload.gdprObjectId !== "";
            const condition_2 = payload.gdprObjectId !== null;

            commit({
                type: "updateValidationData",
                tab_id: "tab_1",
                value: condition_1 && condition_2,
            });
        },
        processGdprObjectType({commit}, payload) {
            commit({
                type: "updateGdprObjectType",
                gdprObject: payload.gdprObject,
            })

            // Get validation conditions
            const condition_1 = payload.gdprObjectType !== "";
            const condition_2 = payload.gdprObjectType !== null;

            commit({
                type: "updateValidationData",
                tab_id: "tab_0",
                value: condition_1 && condition_2,
            });

            //Reset gdpr id
            commit({
                type: "updateGdprObjectId",
                gdprObjectId: 0,
            });
        },
    },
    getters: {
        getGdprObjectId: (state) => {
            return state.gdprObjectId;
        },
        getGdprObjectType: (state) => {
            return state.gdprObjectType;
        },
        getUserActionToRemove: (state) => {
            return state.userActionToRemove;
        },
        getValidationData: (state) => {
            return state.validationData;
        },
    },
}
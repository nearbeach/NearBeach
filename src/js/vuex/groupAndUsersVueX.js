export const moduleGroupsAndUsers = {
    state: () => ({
        addingGroupStatus: false,
        addingUserStatus: false,
        objectGroupList: [],
        objectUserList: [],
        potentialGroupList: [],
        potentialUserList: [],
    }),
    mutations: {
        updateGroupsAndUsers(state, payload) {
            //Only update the data if it is defined.
            state.objectGroupList = payload.objectGroupList !== undefined ? payload.objectGroupList : state.objectGroupList;
            state.objectUserList = payload.objectUserList !== undefined ? payload.objectUserList : state.objectUserList;
            state.potentialGroupList = payload.potentialGroupList !== undefined ? payload.potentialGroupList : state.potentialGroupList;
            state.potentialUserList = payload.potentialUserList !== undefined ? payload.potentialUserList : state.potentialUserList;
        },
        updateAddingGroupStatus(state, payload) {
            state.addingGroupStatus = payload.addingGroupStatus;
        },
        updateAddingUserStatus(state, payload) {
            state.addingUserStatus = payload.addingUserStatus;
        }
    },
    actions: {},
    getters: {
        getAddingGroupStatus: (state) => {
            return state.addingGroupStatus;
        },
        getAddingUserStatus: (state) => {
            return state.addingUserStatus;
        },
        getObjectGroupList: (state) => {
            return state.objectGroupList;
        },
        getObjectUserList: (state) => {
            return state.objectUserList;
        },
        getPotentialGroupList: (state) => {
            return state.potentialGroupList;
        },
        getPotentialUserList: (state) => {
            return state.potentialUserList;
        },
    },
};
//GLOBAL VARIABLES
const GLOBAL_DATE = new Date();
const GLOBAL_END_DATE = new Date(
    GLOBAL_DATE.setDate(GLOBAL_DATE.getDate() + 7)
);
const GLOBAL_RELEASE_DATE = new Date(
    GLOBAL_DATE.setDate(GLOBAL_DATE.getDate() + 7)
);
const GLOBAL_START_DATE = new Date(
    GLOBAL_DATE.setDate(GLOBAL_DATE.getDate() + 7)
);

//Modify the global times.
GLOBAL_END_DATE.setHours(16);
GLOBAL_END_DATE.setMinutes(0);
GLOBAL_END_DATE.setSeconds(0);
GLOBAL_END_DATE.setMilliseconds(0);

GLOBAL_RELEASE_DATE.setHours(17);
GLOBAL_RELEASE_DATE.setMinutes(30);
GLOBAL_RELEASE_DATE.setSeconds(0);
GLOBAL_RELEASE_DATE.setMilliseconds(0);

GLOBAL_START_DATE.setHours(9);
GLOBAL_START_DATE.setMinutes(0);
GLOBAL_START_DATE.setSeconds(0);
GLOBAL_START_DATE.setMilliseconds(0);


export const moduleRfc = {
    state: () => ({
        changeTaskCount: 0,
        endDateModel: GLOBAL_END_DATE.getTime(),
        groupListModel: [],
        releaseDateModel: GLOBAL_RELEASE_DATE.getTime(),
        startDateModel: GLOBAL_START_DATE.getTime(),
        userListModel: [],
    }),
    mutations: {
        updateChangeTaskCount(state, payload) {
            //Update the count
            state.changeTaskCount = payload.changeTaskCount;
        },
        updateGroupList(state, payload) {
            //Update the group list model
            state.groupListModel = payload.groupList;
        },
        updateRfcDates(state, payload) {
            state.endDateModel = payload.endDateModel;
            state.releaseDateModel = payload.releaseDateModel;
            state.startDateModel = payload.startDateModel;
        },
        updateRfcReleaseDate(state, payload) {
            state.releaseDateModel = payload.releaseDateModel;
        },
    },
    actions: {},
    getters: {
        getChangeTaskCount: (state) => {
            return state.changeTaskCount;
        },
        getEndDate: (state) => {
            return state.endDateModel;
        },
        getReleaseDate: (state) => {
            return state.releaseDateModel;
        },
        getStartDate: (state) => {
            return state.startDateModel;
        },
    },
};

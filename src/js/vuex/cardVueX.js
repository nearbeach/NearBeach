const axios = require('axios');

export const moduleCard = {
    state: () => ({
        cardId: 0,
        cardTitle: "",
        cardColumn: 0,
        cardLevel: 0,
        cardLink: {},
        cardDescription: "",
        cardNotes: [],
        cardPriority: 2,
        kanbanStatus: "Open",
        listColumns: [],
        listLevels: [],
        userList: [],
    }),
    mutations: {
        updateKanbanStatus(state, payload) {
            state.kanbanStatus = payload.kanbanStatus;
        },
        updateValue(state, payload) {
            state[payload.field] = payload.value;
        },
        updateLists(state, payload) {
            state.listColumns = payload.columnResults.map((row) => {
                return {
                    value: row.pk,
                    label: row.fields.kanban_column_name,
                };
            });
            state.listLevels = payload.levelResults.map((row) => {
                return {
                    value: row.pk,
                    label: row.fields.kanban_level_name,
                };
            });
        },
        updateUserList(state, payload) {
            state.userList = payload.userList;
        },
    },
    actions: {
        updateCard({commit, state}, payload) {
            state.cardId = payload.cardId;
            state.cardTitle = payload.cardTitle;
            state.cardDescription = payload.cardDescription;
            state.cardLevel = payload.cardLevel;
            state.cardColumn = payload.cardColumn;
            state.cardLink = payload.cardLink;
            state.cardPriority = payload.cardPriority;

            //Get data for the notes
            axios.post(
                `/object_data/kanban_card/${payload.cardId}/note_list/`,
                {},
                {
                    xsrfCookieName: 'csrftoken',
                    xsrfHeaderName: 'X-CSRFTOKEN',
                }
            ).then((response) => {
                //Save the data into noteHistoryResults
                //state.cardNotes = response.data;
                commit("initNoteList", {
                    noteList: response.data,
                });
            });

            //Get data for the user list
            axios.post(
                `/object_data/kanban_card/${payload.cardId}/group_and_user_data/`,
                {},
                {
                    xsrfCookieName: 'csrftoken',
                    xsrfHeaderName: 'X-CSRFTOKEN',
                }
            ).then((response) => {
                //Save the data into userList
                commit('updateGroupsAndUsers', {
                    objectGroupList: response.data.object_group_list,
                    objectUserList: response.data.object_user_list,
                    potentialGroupList: response.data.potential_group_list,
                    potentialUserList: response.data.potential_user_list,
                })
            });
        },
    },
    getters: {
        getAllCardData: (state) => {
            return {
                cardId: state.cardId,
                cardTitle: state.cardTitle,
                cardDescription: state.cardDescription,
                cardLevel: state.cardLevel,
                cardColumn: state.cardColumn,
                cardPriority: state.cardPriority,
            };
        },
        getCardId: (state) => {
            return state.cardId;
        },
        getCardColumn: (state) => {
            return state.cardColumn;
        },
        getCardLevel: (state) => {
            return state.cardLevel;
        },
        getCardLink: (state) => {
            return state.cardLink;
        },
        getCardTitle: (state) => {
            return state.cardTitle;
        },
        getKanbanStatus: (state) => {
            return state.kanbanStatus;
        },
        getListColumns: (state) => {
            return state.listColumns;
        },
        getListLevels: (state) => {
            return state.listLevels;
        },
        getCardNotes: (state) => {
            return state.cardNotes;
        },
        getUserList: (state) => {
            return state.userList;
        },
        getCardPriority: (state) => {
            return state.cardPriority;
        },
    },
};
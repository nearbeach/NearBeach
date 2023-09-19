export const moduleKanban = {
    state: () => ({
        kanbanCardResults: [],
        columnResults: [],
        levelResults: [],
        openCardOnLoad: 0,
    }),
    mutations: {
        //CRUD Operations
        addCard(state, payload) {
            state.kanbanCardResults.push(payload.newCard[0]);
        },
        archiveCard(state, payload) {
            const cardId = payload.cardId;

            //Filter out the card with the card id
            state.kanbanCardResults = state.kanbanCardResults.filter((row) => {
                return row.pk !== parseInt(cardId, 10);
            });
        },
        archiveCards(state, payload) {
            //payload will contain both column and level values
            const column = payload.column,
                level = payload.level;

            //Filter out the column/level cards - and update the kanban card results
            state.kanbanCardResults = state.kanbanCardResults.filter((row) => {
                //Check to see if the column and level match
                const boolean_column =
                        parseInt(row.fields.kanban_column, 10) === column,
                    boolean_level =
                        parseInt(row.fields.kanban_level, 10) === level;

                //If they both match - exclude them from the data;
                return !(boolean_column && boolean_level);
            });
        },
        updateKanbanCard(state, payload) {
            //Get the index location
            const index_location = state.kanbanCardResults.findIndex((row) => {
                return row.pk === parseInt(payload.card_id, 10);
            });

            //Loop through each keys for the payload, and update the relevant field
            const continue_keys = ["type", "card_id"];
            Object.keys(payload).forEach((key) => {
                //Skip some certain keys
                if (continue_keys.includes(key)) {
                    return;
                }

                //Update the results
                state.kanbanCardResults[index_location].fields[key] =
                    payload[key];
            });
        },
        //The initial payload of kanban card results
        initPayload(state, payload) {
            state.kanbanCardResults = payload.kanbanCardResults;
            state.columnResults = payload.columnResults;
            state.levelResults = payload.levelResults;
            state.openCardOnLoad = payload.openCardOnLoad;
        },
    },
    actions: {},
    getters: {
        getCards: (state) => {
            return state.kanbanCardResults;
        },
        getColumnResults: (state) => {
            return state.columnResults;
        },
        getLevelResults: (state) => {
            return state.levelResults;
        },
        getLevelCardCount: (state) => (level_id) => {
            return state.kanbanCardResults.filter((row) => {
                return row.fields.kanban_level === level_id;
            }).length;
        },
        getOpenCardOnLoad: (state) => {
            return state.openCardOnLoad;
        },
    },
};

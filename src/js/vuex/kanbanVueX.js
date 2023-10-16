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
    actions: {
        async dragDifferentColumn({dispatch, commit, state}, payload) {
            //Required Data
            const event = payload.event;

            var new_elem = event.to,
                old_elem = event.from,
                card_id = event.item.dataset.cardId;

            //Setup variables (for shorthand)
            let new_card_column = new_elem.dataset.column,
                new_card_level = new_elem.dataset.level,
                new_card_sort_number = event.newIndex - 1,
                old_card_column = old_elem.dataset.column,
                old_card_level = old_elem.dataset.level;

            // 1. Grab all old column/level location cards - and reorder
            const reorder_old_cards = state.kanbanCardResults.filter(row => {
                //The columns, levels match. And the primary key is NOT the card id
                const condition_1 = row.fields.column === old_card_column;
                const condition_2 = row.fields.level === old_card_level;
                const condition_3 = row.pk !== card_id;

                return condition_1 && condition_2 && condition_3;
            }).sort((a, b) => a.fields.kanban_card_sort_number - b.fields.kanban_card_sort_number);

            // 2. Update the ordering
            reorder_old_cards.forEach((row, index) => {
                this.$store.commit({
                    type: "updateKanbanCard",
                    card_id: row.pk,
                    kanban_card_sort_number: index,
                });
            });

            // 3. Update the card's information
            commit({
                type: "updateKanbanCard",
                card_id: card_id,
                kanban_column: new_card_column,
                kanban_level: new_card_level,
                kanban_card_sort_number: new_card_sort_number,
            });

            // 4. Filter for the new column/level location cards
            // For all cards that have a sort order >= new_card_sort_number
            // We want to increase by 1
            const reorder_new_cards = state.kanbanCardResults.filter(row => {
                //The columns, levels match. And the primary key is NOT the card id
                const condition_1 = row.fields.column === new_card_column;
                const condition_2 = row.fields.level === new_card_level;
                const condition_3 = row.pk !== card_id;

                return condition_1 && condition_2 && condition_3;
            }).sort((a, b) => a.fields.kanban_card_sort_number - b.fields.kanban_card_sort_number);

            // 2. Update the ordering
            reorder_new_cards.forEach((row, index) => {
                // If the index is equal or greater than the card sort number - we'll have to add +1 to it.
                let i = index;
                if (index >= new_card_sort_number) i = i + 1;

                commit({
                    type: "updateKanbanCard",
                    card_id: row.pk,
                    kanban_card_sort_number: i,
                });
            });
        },
        async dragSameColumn({dispatch, commit}, payload) {},
        async kanbanCardMoved({dispatch}, payload) {
            const event = payload.event;

            if (event === undefined) return;

            //Determine if we are dragging to the same or different location
            var new_elem = event.to,
                old_elem = event.from;

            //Setup variables (for shorthand)
            let new_card_column = new_elem.dataset.column,
                new_card_level = new_elem.dataset.level,
                old_card_column = old_elem.dataset.column,
                old_card_level = old_elem.dataset.level;

            //Depending if the card moves columns depends what we do
            if (
                new_card_column === old_card_column &&
                new_card_level === old_card_level
            ) {
                await dispatch("dragSameColumn", payload);
            } else {
                await dispatch("dragDifferentColumn", payload);
            }
        },
    },
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

import axios from "axios";

export const kanbanSettings = {
    state: () => ({
        canDragCards: true,
        levels: [],
    }),
    mutations: {
        initKanbanSettings (state, payload) {
            state.canDragCards = payload.canDragCards;
            state.levels = payload.levels;
        },
        updateCanDragCards(state, payload) {
            //Updating canDragCards
            state.canDragCards = payload.canDragCards;
        },
        updateLevels(state, payload) {
            state.levels = payload.levels;
        },
    },
    actions: {
        async updateCanDragCards({ dispatch, commit }, payload) {
            //Wait for the data to finish updating
            await commit("updateCanDragCards", {
                canDragCards: payload.canDragCards,
            });

            //Update the backend
            dispatch("updateSettingsBackend");
        },
        async updateLevelCollapse({ dispatch, commit, state }, payload) {
            //Map in the changes
            let current_levels = state.levels.map((row) => {
                //If the payload.level_id != row.level_id, just return the data
                if (payload.level_id !== row.level_id) return row;

                // Return the new structure
                return {
                    levelId: payload.levelId,
                    isCollapsed: payload.isCollapsed,
                }
            })

            //Commit the state
            await commit("updateLevels", {
               levels: current_levels,
            });

            //ADD CODE TO UPDATE BACKEND :)
            dispatch("updateSettingsBackend");
        },
        updateSettingsBackend({ state }) {
            //Grab the data and use axios to tell the backend to update the data
        }
    },
    getters: {
        getCanDragCards: (state) => {
            return state.canDragCards;
        },
        getLevelCollapseStatus: (state) => (level_id) => {
            //Filter for the level
            const level_results = state.levels.filter(row => {
                return row.level_id = level_id;
            });

            //If array is empty - return default false
            if (level_results.length === 0) return false;

            //Return the first level results
            return level_results[0].isCollapsed;
        },
    },
}
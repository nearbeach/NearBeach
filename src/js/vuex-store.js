// import Vuex from 'vuex';
import { createStore } from 'vuex'

const moduleCard = {
  state: () => ({
    cardId: 0,
    cardTitle: '',
    cardColumn: 0,
    cardLevel: 0,
    cardDescription: '',
    cardNotes: [],
    listColumns: [],
    listLevels: [],
  }),
  mutations: {
    appendNote(state, payload) {
      state.cardNotes.push(payload.newNote);
    },
    updateCard(state, payload) {
      state.cardId = payload.cardId;
      state.cardTitle = payload.cardTitle;
      state.cardDescription = payload.cardDescription;
      try {
        //Filter for the correct column data from the list columns
        state.cardColumn = state.listColumns.filter((row) => {
          return payload.cardColumn == row.value;
        })[0];

        //Filter for the correct level data from the list level
        state.cardLevel = state.listLevels.filter((row) => {
          return payload.cardLevel == row.value;
        })[0];
      } catch {
        state.cardColumn = 0;
        state.cardLevel = 0;
      }
      //state.cardLevel = payload.cardLevel;
      //state.cardColumn = payload.cardColumn;

      //Get data for the notes
      axios
        .post(`/object_data/kanban_card/${payload.cardId}/note_list/`)
        .then((response) => {
          //Save the data into noteHistoryResults
          state.cardNotes = response.data;
        })
        .catch((error) => {});
    },
    updateValue(state, payload) {
      state.payload.field = payload.value;
    },
    updateLists(state, payload) {
      state.listColumns = payload.columnResults.map((row) => {
        return {
          value: row.pk,
          column: row.fields.kanban_column_name,
        };
      });
      state.listLevels = payload.levelResults.map((row) => {
        return {
          value: row.pk,
          level: row.fields.kanban_level_name,
        };
      });
    },
  },
  actions: {},
  getters: {
    getAllCardData: (state) => {
      return {
        cardId: state.cardId,
        cardTitle: state.cardTitle,
        cardDescription: state.cardDescription,
        cardLevel: state.cardLevel,
        cardColumn: state.cardColumn,
      };
    },
    getCardId: (state) => {
      return state.cardId;
    },
    getCardNotes: (state) => {
      return state.cardNotes;
    },
  },
};

const moduleDestination = {
  state: () => ({
    destination: 'unknown',
    locationId: 0,
  }),
  mutations: {
    updateDestination(state, payload) {
      state.destination = payload.destination;
      state.locationId = payload.locationId;
    },
  },
  actions: {},
  getters: {
    getDestination: (state) => {
      return state.destination;
    },
    getLocationId: (state) => {
      return state.locationId;
    },
  },
};

const moduleKanban = {
  state: () => ({
    kanbanCardResults: [],
    columnResults: [],
    levelResults: [],
  }),
  mutations: {
    //CUD Operations
    addCard(state, payload) {
      state.kanbanCardResults.push(payload.newCard[0]);
    },
    archiveCards(state, payload) {
        //payload will contain both column and level values
        const column = payload.column,
            level = payload.level;

        //Filter out the column/level cards - and update the kanban card results
        state.kanbanCardResults = state.kanbanCardResults.filter(row => {
            //Check to see if the column and level match
            const boolean_column = parseInt(row['fields']['kanban_column'], 10) === column,
                boolean_level = parseInt(row['fields']['kanban_level'], 10) === level;



            //If they both match - exclude them from the data;
            return !(boolean_column && boolean_level);
        });
    },
    updateKanbanCard(state, payload) {
      //Get the index location
      const index_location = state.kanbanCardResults.findIndex((row) => {
        return row.pk == payload.card_id;
      });

      //Loop through each keys for the payload, and update the relevant field
      const continue_keys = ['type', 'card_id'];
      Object.keys(payload).forEach((key) => {
        //Skip some certain keys
        if (continue_keys.includes(key)) {
          return;
        }

        //Update the results
        state.kanbanCardResults[index_location].fields[key] = payload[key];
      });
    },
    deletedCard(state, payload) {},

    //The initial payload of kanban card results
    initPayload(state, payload) {
      state.kanbanCardResults = payload.kanbanCardResults;
      state.columnResults = payload.columnResults;
      state.levelResults = payload.levelResults;
    },
  },
  actions: {},
  getters: {
    getCards: (state) => {
      return state.kanbanCardResults;
    },
    getColumns: (state) => {
      return state.columnResults;
    },
  },
};

const moduleUrl = {
  state: () => ({
    rootUrl: '/',
    staticUrl: '/static/',
  }),
  mutations: {
    updateUrl(state, payload) {
      state.rootUrl = payload.rootUrl;
      state.staticUrl = payload.staticUrl;
    },
  },
  actions: {},
  getters: {
    getRootUrl: (state) => {
      return state.rootUrl;
    },
    getStaticUrl: (state) => {
      return state.staticUrl;
    },
  },
};

const moduleUserLevel = {
  state: () => ({
    userLevel: 0,
  }),
  mutations: {
    updateUserLevel(state, payload) {
      state.userLevel = payload.userLevel;
    },
  },
  action: {},
  getters: {
    getUserLevel: (state) => {
      return state.userLevel;
    },
  },
}

export const store = createStore({
  modules: {
    card: moduleCard,
    destination: moduleDestination,
    kanban: moduleKanban,
    url: moduleUrl,
    userLevel: moduleUserLevel,
  },
});
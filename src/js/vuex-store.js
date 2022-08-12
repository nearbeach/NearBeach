// import Vuex from 'vuex';
import { createStore } from 'vuex'
import axios from 'axios';

//GLOBAL VARIABLES
var GLOBAL_DATE = new Date();
var GLOBAL_END_DATE = new Date(GLOBAL_DATE.setDate(GLOBAL_DATE.getDate() + 7));
var GLOBAL_RELEASE_DATE = new Date(GLOBAL_DATE.setDate(GLOBAL_DATE.getDate() + 7));
var GLOBAL_START_DATE = new Date(GLOBAL_DATE.setDate(GLOBAL_DATE.getDate() + 7));

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

const moduleCard = {
  state: () => ({
    cardId: 0,
    cardTitle: '',
    cardColumn: 0,
    cardLevel: 0,
    cardLink: {},
    cardDescription: '',
    cardNotes: [],
    kanbanStatus: "Open",
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
      state.cardLevel = payload.cardLevel;
      state.cardColumn = payload.cardColumn;
      state.cardLink = payload.cardLink;

      //Get data for the notes
      axios
        .post(`/object_data/kanban_card/${payload.cardId}/note_list/`)
        .then((response) => {
          //Save the data into noteHistoryResults
          state.cardNotes = response.data;
        })
        .catch((error) => {});
    },
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

const moduleRfc = {
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

      //Contact the API to get the list of users connected to this group
      //'object_data/request_for_change/<location_id>/user_list_all/',
      axios.post(
        `/object_data/request_for_change/${this.state.locationId}/user_list_all/`
      ).then(response => {
      })
    },
    updateRfcDates(state, payload) {
      state.endDateModel = payload.endDateModel;
      state.releaseDateModel = payload.releaseDateModel;
      state.startDateModel = payload.startDateModel;
    }
  },
  actions: {},
  getters: {
    getChangeTaskCount: (state) => {
      return state.changeTaskCount;
    },
    getEndDate: (state) => {
      return state.endDateModel;
    },
    getReleaseDateModel: (state) => {
      return state.releaseDateModel;
    },
    getStartDate: (state) => {
      return state.startDateModel;
    }
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
    rfc: moduleRfc,
    url: moduleUrl,
    userLevel: moduleUserLevel,
  },
});

export const moduleDestination = {
    state: () => ({
        destination: "unknown",
        locationId: 0,
        title: "",
    }),
    mutations: {
        updateDestination(state, payload) {
            state.destination = payload.destination;
            state.locationId = payload.locationId;
        },
        updateTitle(state, payload) {
            state.title = payload.title;
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
        getTitle: (state) => {
            return state.title;
        },
    },
};
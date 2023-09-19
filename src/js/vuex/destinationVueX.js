export const moduleDestination = {
    state: () => ({
        destination: "unknown",
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
export const moduleObjectLink = {
    state: () => ({
        objectLink: {
            objectId: 0,
            link_relationship: "",
            parent_link: "",
            object_title: "",
            object_status: "",
            object_type: "",
        },
    }),
    mutations: {
        updateObjectLink(state, payload) {
            state.objectLink = payload.objectLink;
        }
    },
    action: {},
    getters: {
        getObjectLink: (state) => {
            return state.objectLink;
        }
    },
}
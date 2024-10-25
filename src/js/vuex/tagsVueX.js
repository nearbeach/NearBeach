export const moduleTags = {
    state: () => ({
        allTagList: [],
        assignedTags: [],
    }),
    mutations: {
        updateAllTagList: (state, payload) => {
            state.allTagList = payload.allTagList;
        },
        updateAssignedTags: (state, payload) => {
            state.assignedTags = payload.assignedTags;
        },
    },
    actions: {
        removeAssignedTag: ({commit, state}, payload) => {
            const assigned_tags = state.assignedTags.filter((row) => {
                return row.tag_id !== payload.tag_id;
            });

            commit({
                type: "updateAssignedTags",
                assignedTags: assigned_tags,
            })
        },
    },
    getters: {
        getAllTagList: (state) => {
            return state.allTagList;
        },
        getAssignedTags: (state) => {
            return state.assignedTags;
        },
        getAvailableTagList: (state) => {
            return state.allTagList.filter((row) => {
                return !state.assignedTags.some((tag) =>
                    tag.tag_id === parseInt(row.value));
            });
        },
    },
}

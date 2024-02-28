export const moduleNote = {
    state: () => ({
        noteDescription: "",
        noteId: 0,
        noteList: [],
    }),
    mutations: {
        addNote(state, payload) {
            state.noteList.push(payload.newNote);
        },
        initNoteList(state, payload) {
            state.noteList = payload.noteList;
        },
        removeNote(state, payload) {
            state.noteList = state.noteList.filter((row) => {
                return parseInt(row.object_note_id) !== parseInt(payload.noteId);
            });
        },
    },
    actions: {
        editSingleNote({state}, payload) {
            //Get the index of the array
            const index = state.noteList.findIndex((row) => {
                return parseInt(row.object_note_id) === parseInt(payload.noteId);
            });

            //If there are no indexes, escape
            if (index < 0 ) return;

            //Update the note description
            let mutate_data = state.noteList;
            mutate_data[index].object_note = payload.noteDescription;

            //Update state
            state.noteList = mutate_data;
        },
        updateNoteId({commit, state}, payload) {
            //Update the node id
            state.noteId = payload.noteId;

            const filtered_data = state.noteList.filter((row) => {
                return parseInt(row.object_note_id) === parseInt(payload.noteId);
            })

            if (filtered_data.length === 0) {
                //Set description to empty and return
                state.noteDescription = "";
                return;
            }

            //Update note description
            state.noteDescription = filtered_data[0].object_note;
        },
    },
    getters: {
        getNoteList: (state) => {
            return state.noteList;
        },
        getSingleNoteDescription: (state)  => {
            return state.noteDescription;
        },
        getSingleNoteId: (state) => {
            return state.noteId;
        },
    },
}
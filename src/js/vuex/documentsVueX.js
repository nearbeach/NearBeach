export const moduleDocuments = {
    state: () => ({
        acceptedDocuments: "image/*,text/*,.pdf,.doc,.docx,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        currentFolder: 0,
        documentList: [],
        documentRemoveKey: "",
        folderList: [],
        folderRemoveId: "",
    }),
    mutations: {
        updateCurrentFolder: (state, payload) => {
            //Add in a simple check for the current folder - default to 0
            let current_folder = payload.currentFolder;
            if (current_folder === null || current_folder === undefined) current_folder = 0;

            state.currentFolder = current_folder;
        },
        updateDocumentList: (state, payload) => {
            state.documentList = payload.documentList;
        },
        updateDocumentRemoveKey: (state, payload) => {
            state.documentRemoveKey = payload.documentRemoveKey;
        },
        updateFolderList: (state, payload) => {
            state.folderList = payload.folderList;
        },
        updateFolderRemoveId: (state, payload) => {
            state.folderRemoveId = payload.folderRemoveId;
        },
    },
    actions: {
        appendDocumentList: ({state, commit}, payload) => {
            //Append data to existing document list
            const new_document = payload.documentList;
            const document_list = state.documentList;
            document_list.push(new_document);

            //Commit new document list
            commit({
                type: "updateDocumentList",
                documentList: document_list,
            });
        },
        appendFolderList: ({state, commit}, payload) => {
            //Append data to existing folder list
            const new_folder = payload.folderList;
            const folder_list = state.folderList;
            folder_list.push(new_folder);

            //Commit new folder list
            commit({
                type: "updateFolderList",
                folderList: folder_list,
            });
        },
        goToParentDirectory: ({state, commit}) => {
            //Filter for the directory - then obtain it's parent directory
            const filtered_data = state.folderList.filter((row) => {
                return parseInt(row.pk) === parseInt(state.currentFolder);
            })[0];

            //Make sure we have some data
            if (filtered_data === undefined) return;

            //Update the current directory to the parent folder
            commit({
                type: "updateCurrentFolder",
                currentFolder: filtered_data.fields.parent_folder,
            });
        },
        removeDocument: ({state, commit}, payload) => {
            //Filter out the document
            const new_document_list = state.documentList.filter((row) => {
                return row.document_key_id !== payload.document_key;
            });

            //Commit the new document list
            commit({
                type: "updateDocumentList",
                documentList: new_document_list,
            });
        },
        removeFolder: ({state, commit}, payload) => {
            //Filter out the folders
            const new_folder_list = state.folderList.filter((row) => {
                return parseInt(row.pk) !== payload.folder_id;
            });

            //Commit the new folder list
            commit({
                type: "updateFolderList",
                folderList: new_folder_list,
            });
        },
    },
    getters: {
        getAcceptedDocuments: (state) => {
            return state.acceptedDocuments;
        },
        getCurrentFolder: (state) => {
            return state.currentFolder;
        },
        getDocumentFilteredList: (state) => {
            //If current folder set as 0 - filter for none
            let filter_folder = state.currentFolder;
            if (filter_folder === 0) filter_folder = null;

            //Filter the results to contain only the documents in the current folder
			return state.documentList.filter((row) => {
				return row.folder === filter_folder;
			}).sort((a, b) => {
				return a.document_key__document_description > b.document_key__document_description;
			});
        },
        getDocumentObjectCount: (state) => {
            //A simple count, that returns the number of folders and documents
            return state.documentList.length + state.folderList.length;
        },
        getDocumentRemoveKey: (state) => {
            return state.documentRemoveKey;
        },
        getFolderFilteredList: (state) => {
            //If current folder set as 0 - filter for none
            let filter_folder = state.currentFolder;
            if (filter_folder === 0) filter_folder = null;

            //Filter the results to contain only the folders in the current folder
            return state.folderList.filter((row) => {
                return row.fields.parent_folder === filter_folder;
            }).sort((a, b) => {
                return a.fields.folder_description > b.fields.folder_description;
            });
        },
        getFolderRemoveId: (state) => {
            return state.folderRemoveId;
        },
    },
}
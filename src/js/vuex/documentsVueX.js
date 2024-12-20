export const moduleDocuments = {
    state: () => ({
        acceptedDocuments: "image/*,text/*,.pdf,.doc,.docx,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        currentFolder: 0,
        currentParentFolder: 0,
        documentList: [],
        documentRemoveKey: "",
        folderList: [],
        folderRemoveId: "",
    }),
    mutations: {
        updateCurrentFolder: (state, payload) => {
            //Add in a simple check for the current folder - default to 0
            const index_location = state.folderList.findIndex((row) => {
                return row.pk === parseInt(payload.currentFolder);
            });

            let current_folder = 0;
            let parent_folder = 0;
            if (index_location !== undefined && index_location >= 0)
            {
                current_folder = state.folderList[index_location].pk;
                parent_folder = state.folderList[index_location].fields.parent_folder;
                parent_folder = parent_folder === null ? 0 : parent_folder;
            }

            state.currentFolder = current_folder;
            state.currentParentFolder = parent_folder;
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
        updateDocumentFolder: ({state}, payload) => {
            const index_location = state.documentList.findIndex((row) => {
                return row.document_key_id === payload.document_key_id;
            });
            if (index_location === undefined || index_location < 0) return;

            //Update the folder id directly
            state.documentList[index_location].folder = payload.parent_folder_id;
        },
        updateFolderParentFolder: ({state}, payload) => {
            const index_location = state.folderList.findIndex((row) => {
                return parseInt(row.pk) === parseInt(payload.moving_folder_id);
            });
            if (index_location === undefined || index_location < 0) return;

            //Update the folder id directly
            state.folderList[index_location].fields.parent_folder = payload.parent_folder_id;
        },
    },
    getters: {
        getAcceptedDocuments: (state) => {
            return state.acceptedDocuments;
        },
        getCurrentFolder: (state) => {
            return state.currentFolder;
        },
        getCurrentParentFolder: (state) => {
            return state.currentParentFolder;
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
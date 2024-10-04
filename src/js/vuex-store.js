// import Vuex from 'vuex';
import {createStore} from "vuex";

import {moduleArchiveCards} from "./vuex/archiveCardsVueX";
import {moduleCard} from "./vuex/cardVueX";
import {moduleChangeTask} from "./vuex/changeTaskVueX";
import {moduleConfirmDelete} from "./vuex/confirmDeleteVueX";
import {moduleDestination} from "./vuex/destinationVueX";
import {moduleDocuments} from "./vuex/documentsVueX";
import {moduleGantChart} from "./vuex/ganttChartVueX";
import {moduleGroupsAndUsers} from "./vuex/groupAndUsersVueX";
import {moduleKanban} from "./vuex/kanbanVueX";
import {moduleObjectLink} from "./vuex/objectLinkVueX";
import {moduleNewCard} from "./vuex/newCardVueX";
import {moduleNote} from "./vuex/noteVueX";
import {moduleRfc} from "./vuex/rfcVueX";
import {moduleToasts} from "./vuex/toastsVueX";
import {moduleUrl} from "./vuex/urlVueX";
import {moduleUserExtraPermissions} from "./vuex/userExtraPermissionsVueX";
import {moduleUserLevel} from "./vuex/userLevelVueX";


// User settings
import {kanbanSettings} from "./vuex/usersettings/kanbanSettingsVueX";
import {themeSettings} from "./vuex/usersettings/themeSettingsVueX";

export const store = createStore({
    modules: {
        archiveCards: moduleArchiveCards,
        card: moduleCard,
        changeTask: moduleChangeTask,
        confirmDelete: moduleConfirmDelete,
        destination: moduleDestination,
        documents: moduleDocuments,
        ganttChart: moduleGantChart,
        groupsAndUsers: moduleGroupsAndUsers,
        kanban: moduleKanban,
        newCard: moduleNewCard,
        note: moduleNote,
        objectLink: moduleObjectLink,
        rfc: moduleRfc,
        toasts: moduleToasts,
        url: moduleUrl,
        userExtraPermissions: moduleUserExtraPermissions,
        userLevel: moduleUserLevel,

        //User Settings
        kanbanSettings: kanbanSettings,
        themeSettings: themeSettings,
    },
});

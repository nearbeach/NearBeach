// import Vuex from 'vuex';
import { createStore } from "vuex";

import { moduleArchiveCards } from "./vuex/archiveCardsVueX";
import { moduleCard } from "./vuex/cardVueX";
import { moduleChangeTask } from "./vuex/changeTaskVueX";
import { moduleDestination } from "./vuex/destinationVueX";
import { moduleGroupsAndUsers } from "./vuex/groupAndUsersVueX";
import { moduleKanban } from "./vuex/kanbanVueX";
import { moduleObjectLink } from "./vuex/objectLinkVueX";
import { moduleRfc } from "./vuex/rfcVueX";
import { moduleUrl } from "./vuex/urlVueX";
import { moduleUserLevel } from "./vuex/userLevelVueX";

export const store = createStore({
	modules: {
		archiveCards: moduleArchiveCards,
		card: moduleCard,
		changeTask: moduleChangeTask,
		destination: moduleDestination,
		groupsAndUsers: moduleGroupsAndUsers,
		kanban: moduleKanban,
		objectLink: moduleObjectLink,
		rfc: moduleRfc,
		url: moduleUrl,
		userLevel: moduleUserLevel,
	},
});

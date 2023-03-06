// import Vuex from 'vuex';
import { createStore } from "vuex";

import { moduleArchiveCards } from "./vuex/archiveCardsVueX";
import { moduleCard } from "./vuex/cardVueX";
import { moduleDestination } from "./vuex/destinationVueX";
import { moduleKanban } from "./vuex/kanbanVueX";
import { moduleRfc } from "./vuex/rfcVueX";
import { moduleUrl } from "./vuex/urlVueX";
import { moduleUserLevel } from "./vuex/userLevelVueX";

export const store = createStore({
	modules: {
		archiveCards: moduleArchiveCards,
		card: moduleCard,
		destination: moduleDestination,
		kanban: moduleKanban,
		rfc: moduleRfc,
		url: moduleUrl,
		userLevel: moduleUserLevel,
	},
});

import type {UserInterface} from "@/utils/interfaces/stores/UserInterface.ts";
import type {GroupInterface} from "@/utils/interfaces/stores/GroupInterface.ts";
import type {PriorityInterface} from "@/utils/interfaces/stores/PriorityInterface.ts";
import type {StatusInterface} from "@/utils/interfaces/stores/StatusInterface.ts";
import type {OrganisationInterface} from "@/utils/interfaces/stores/OrganisationInterface.ts";

export interface ObjectInterface {
	id: number,
	title: string,
	description: string,
	organisation: OrganisationInterface,
	status: StatusInterface,
	priority: PriorityInterface,
	story_point: number,
	start_date: string,
	end_date: string,
	group_list: GroupInterface[],
	user_list: UserInterface[],
	date_created: string,
	date_modified: string,
}
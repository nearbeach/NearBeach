import type {GroupInterface} from "@/utils/interfaces/stores/GroupInterface.ts";
import type {UserInterface} from "@/utils/interfaces/stores/UserInterface.ts";

export interface GroupAndUserInterface {
    group_list: GroupInterface[],
    potential_user_list: UserInterface[],
    user_list: UserInterface[],
}
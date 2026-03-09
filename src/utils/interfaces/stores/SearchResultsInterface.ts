import type {OrganisationInterface} from "@/utils/interfaces/stores/OrganisationInterface.ts";
import type {PriorityInterface} from "@/utils/interfaces/stores/PriorityInterface.ts";
import type {StatusInterface} from "@/utils/interfaces/stores/StatusInterface.ts";

export interface SearchResultsInterface {
    id: number,
    title: string,
    description: string,
    end_date: string,
    start_date: string,
    organisation: OrganisationInterface,
    priority: PriorityInterface,
    status: StatusInterface,
}
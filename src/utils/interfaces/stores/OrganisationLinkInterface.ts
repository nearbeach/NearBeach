import type {CustomerInterface} from "@/utils/interfaces/stores/CustomerInterface.ts";
import type {OrganisationInterface} from "@/utils/interfaces/stores/OrganisationInterface.ts";

export interface OrganisationLinkInterface {
    id: number,
    customers: null | CustomerInterface[],
    potential_customers: null | CustomerInterface[],
    organisation: OrganisationInterface,
}

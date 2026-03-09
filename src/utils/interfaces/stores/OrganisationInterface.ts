import type {CustomerInterface} from "@/utils/interfaces/stores/CustomerInterface.ts";

export interface OrganisationInterface {
    id: number,
    name: string,
    website: string,
    email: string,
    profile_picture_path: null | string,
    customers: null | CustomerInterface[],
}

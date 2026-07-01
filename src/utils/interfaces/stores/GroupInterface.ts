import type {ParentGroupInterface} from "@/utils/interfaces/stores/ParentGroupInterface.ts";

export interface GroupInterface {
    id: number,
    name: string,
    parent_group: ParentGroupInterface,
}
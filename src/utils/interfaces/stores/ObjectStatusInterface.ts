import type {StatusInterface} from "@/utils/interfaces/stores/StatusInterface.ts";

export interface ObjectStatusInterface {
    requirement: StatusInterface[],
    requirement_item: StatusInterface[],
    project: StatusInterface[],
    task: StatusInterface[],
}
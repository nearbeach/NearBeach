import type {ObjectInterface} from "@/utils/interfaces/stores/ObjectInterface.ts";

export interface SprintLinkInterface {
    id: string,
    title: string,
    requirement: ObjectInterface[],
    project: ObjectInterface[],
    total_story_points: number,
    completed_story_points: number,
    status: string,
    start_date: string,
    end_date: string,
}
import type {TitleInterface} from "@/utils/interfaces/stores/TitleInterface.ts";

export interface CustomerInterface {
    id: number;
    title: TitleInterface,
    first_name: string,
    last_name: string,
    email: string,
}
import type {CustomerInterface} from "@/utils/interfaces/stores/CustomerInterface.ts";

export interface ResponseInterface {
    count: number,
    next: null | number,
    previous: null | number,
    results: null | CustomerInterface[],
}
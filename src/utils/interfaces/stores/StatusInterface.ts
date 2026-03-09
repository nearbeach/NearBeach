import type {HigherOrderStatusInterface} from "@/utils/interfaces/stores/HigherOrderStatusInterface.ts";

export interface StatusInterface {
    id: number,
    status: string,
    higher_order_status: HigherOrderStatusInterface,
}
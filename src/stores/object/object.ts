// store/object.ts
import { defineStore } from 'pinia'

export const useObjectStore = defineStore('object', {
    state: () => {
        return {
            description: "",
            end_date: null,
            group_list: [],
            id: 0,
            organisation: {},
            priority: {
                value: 0,
                label: "",
            },
            start_date: null,
            // TODO - do we really need all this extra data for the status?
            // It'll be easier for everyone if we add the status as a model directly
            // However we lose key information like "higher order status"
            status: {
                id: 0,
                status: "",
                higher_order_status: {
                    value: "",
                    label: "",
                }
            },
            story_points: 0,
            title: "",
            user_list: [],
        }
    },
});
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
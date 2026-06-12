// store/object.ts
import {defineStore} from 'pinia'

export const useObjectStore = defineStore('object', {
    state: () => ({
        description: "",
        destination: "",
        end_date: null,
        group_list: [],
        id: 0,
        is_loaded: false,
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
    }),
    actions: {
        resetObject() {
            this.description = "";
            this.destination = "";
            this.end_date = null;
            this.group_list = [];
            this.id = 0;
            this.is_loaded = false;
            this.organisation = {};
            this.priority = {
                value: 0,
                label: "",
            };
            this.start_date = null;
            this.status = {
                id: 0,
                status: "",
                higher_order_status: {
                    value: "",
                    label: "",
                }
            };
            this.story_points = 0;
            this.title = "";
            this.user_list = [];
        }
    }

});
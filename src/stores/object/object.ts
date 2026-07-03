// store/object.ts
import {defineStore} from 'pinia'
import type {GroupInterface} from "@/utils/interfaces/stores/GroupInterface.ts";
import type {UserInterface} from "@/utils/interfaces/stores/UserInterface.ts";

export const useObjectStore = defineStore('object', {
    state: () => ({
        description: "",
        destination: "",
        end_date: null,
        group_list: [] as GroupInterface[],
        id: 0,
        is_loaded: false,
        organisation: {},
        potential_user_list: [] as UserInterface[],
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
        user_list: [] as UserInterface[],
    }),
    actions: {
        removeGroup(group_id: number) {
            this.group_list = this.group_list.filter((row) => {
                return row.id !== group_id;
            });
        },
        removeUser(user_id: number) {
            this.user_list = this.user_list.filter((row) => {
                return row.id !== user_id;
            });
        },
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
    },
    getters: {
        fetchArrayOfGroupIds: (state) => {
            return state.group_list.map((row) => {
                return row.id;
            });
        },
    }
});
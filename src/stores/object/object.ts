// store/object.ts
import {defineStore} from 'pinia'
import type {GroupInterface} from "@/utils/interfaces/stores/GroupInterface.ts";
import type {UserInterface} from "@/utils/interfaces/stores/UserInterface.ts";
import type {OrganisationInterface} from "@/utils/interfaces/stores/OrganisationInterface.ts";
import type {CustomerInterface} from "@/utils/interfaces/stores/CustomerInterface.ts";

export const useObjectStore = defineStore('object', {
    state: () => ({
        customers: [] as CustomerInterface[],
        description: "",
        destination: "",
        end_date: null,
        group_list: [] as GroupInterface[],
        id: 0,
        is_loaded: false,
        organisation: {} as OrganisationInterface | null,
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
            this.customers = [];
            this.description = "";
            this.destination = "";
            this.end_date = null;
            this.group_list = [];
            this.id = 0;
            this.is_loaded = false;
            this.organisation = null;
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
        availableUsersToAdd: (state) => {
            // Send back a list of users that are not in user list
            return state.potential_user_list.filter((row: UserInterface) => {
                return !state.user_list.some(user => row.id === user.id);
            });
        },
        fetchArrayOfGroupIds: (state) => {
            return state.group_list.map((row) => {
                return row.id;
            });
        },
    }
});
// store/object_meta_data.ts
import { defineStore } from 'pinia';
import type {StatusInterface} from "@/utils/interfaces/stores/StatusInterface.ts";
import type {TagsInterface} from "@/utils/interfaces/stores/TagsInterface.ts";
import type {TypesInterface} from "@/utils/interfaces/stores/TypesInterface.ts";
import type {ObjectStatusInterface} from "@/utils/interfaces/stores/ObjectStatusInterface.ts";
import type {ObjectTypesInterface} from "@/utils/interfaces/stores/ObjectTypesInterface.ts";
import type {GroupInterface} from "@/utils/interfaces/stores/GroupInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import type {OrganisationInterface} from "@/utils/interfaces/stores/OrganisationInterface.ts";
import type {CustomerInterface} from "@/utils/interfaces/stores/CustomerInterface.ts";

export const useObjectMetaDataStore = defineStore('object_meta_data', {
    state: () => {
        return {
            all_groups: [] as GroupInterface[],
            is_loaded: false as boolean,
            object_status: {
                requirement: [],
                requirement_item: [],
                project: [],
                task: [],
            } as ObjectStatusInterface,
            object_types: {
                requirement: [],
                requirement_item: [],
            } as ObjectTypesInterface,
            organisations: [] as OrganisationInterface[],
            potential_customers: [] as CustomerInterface[],
            tags: [] as TagsInterface[],
            status: [] as StatusInterface[],
            type: [] as TypesInterface[],
        }
    },
    actions: {
        fetchStatus(id: number) {
            return this.status.filter(row => row.id === id);
        },
        updateObjectStatus(destination: string) {
            this.status = this.object_status[destination as keyof ObjectStatusInterface] ?? [];
        },
        updateObjectTypes(destination: string) {
            this.type = this.object_types[destination as keyof ObjectTypesInterface] ?? [];
        },
    },
    getters: {
        availableGroupsToAdd: (state) => {
            // Fetch all group ids for current object
            const objectStore = useObjectStore();
            const excludeIds = objectStore.fetchArrayOfGroupIds;

            // Send back a list of groups that are not in the exclude id list
            return state.all_groups.filter((row) => {
                return !excludeIds.some((id) => row.id === id);
            });
        },
    }
})
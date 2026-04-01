// store/object_meta_data.ts
import { defineStore } from 'pinia';
import type {StatusInterface} from "@/utils/interfaces/stores/StatusInterface.ts";
import type {TagsInterface} from "@/utils/interfaces/stores/TagsInterface.ts";
import type {TypesInterface} from "@/utils/interfaces/stores/TypesInterface.ts";
import type {ObjectStatusInterface} from "@/utils/interfaces/stores/ObjectStatusInterface.ts";
import type {ObjectTypesInterface} from "@/utils/interfaces/stores/ObjectTypesInterface.ts";

export const useObjectMetaDataStore = defineStore('object_meta_data', {
    state: () => {
        return {
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
})
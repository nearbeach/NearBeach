import { beforeEach, describe, expect, test } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import { useObjectStore } from "@/stores/object/object.ts";

const open = { id: 1, status: "Open", higher_order_status: { value: "open", label: "Open" } };
const done = { id: 2, status: "Done", higher_order_status: { value: "closed", label: "Closed" } };
const bug = { id: 7, title: "Bug" };

describe("Object meta data store", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
    });

    test("fetchStatus returns the matching status", () => {
        const store = useObjectMetaDataStore();
        store.status = [open, done];

        expect(store.fetchStatus(2)).toEqual([done]);
        expect(store.fetchStatus(99)).toEqual([]);
    });

    test("updateObjectStatus loads the statuses for a destination", () => {
        const store = useObjectMetaDataStore();
        store.object_status = { requirement: [], requirement_item: [], project: [open], task: [done] } as never;

        store.updateObjectStatus("project");
        expect(store.status).toEqual([open]);

        store.updateObjectStatus("task");
        expect(store.status).toEqual([done]);
    });

    test("updateObjectStatus gives an empty list for an unknown destination", () => {
        const store = useObjectMetaDataStore();
        store.status = [open];

        store.updateObjectStatus("unknown");

        expect(store.status).toEqual([]);
    });

    test("updateObjectTypes loads the types for a destination", () => {
        const store = useObjectMetaDataStore();
        store.object_types = { requirement: [bug], requirement_item: [] } as never;

        store.updateObjectTypes("requirement");

        expect(store.type).toEqual([bug]);
    });

    test("updateObjectTypes gives an empty list for an unknown destination", () => {
        const store = useObjectMetaDataStore();
        store.type = [bug] as never;

        store.updateObjectTypes("project");

        expect(store.type).toEqual([]);
    });

    test("availableGroupsToAdd leaves out the groups already on the object", () => {
        const store = useObjectMetaDataStore();
        store.all_groups = [
            { id: 1, name: "One", parent_group: null },
            { id: 2, name: "Two", parent_group: null },
        ];
        useObjectStore().group_list = [{ id: 1, name: "One", parent_group: null }];

        expect(store.availableGroupsToAdd.map((group) => group.id)).toEqual([2]);
    });
});

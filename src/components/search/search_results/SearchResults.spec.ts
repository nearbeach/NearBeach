import {beforeEach, describe, expect, test} from "vitest";
import {mount, flushPromises} from "@vue/test-utils";
import {SearchResults} from ".";
import {createPinia, setActivePinia} from "pinia";
import {createRouter, createMemoryHistory} from "vue-router";
import i18n from "@/i18n.ts";
import {defineComponent, h} from "vue";
import {useSearchStore} from "@/stores/search/search.ts";

const router = createRouter({
    history: createMemoryHistory(),
    routes: [
        {
            path: "/search",
            meta: {destination: "test-destination"},
            component: defineComponent({render: () => h("div")}),
        },
    ],
});

describe("SearchResults", () => {
    beforeEach(async () => {
        setActivePinia(createPinia());
        await router.push("/search");
        await router.isReady();
    });

    test("renders SearchCard components for each search result", async () => {
        const store = useSearchStore();
        store.searchResults = [
            {
                "id": 1,
                "title": "Test 1",
                "description": "<p>Adding in some rich text into here. The next thing we should do is implement the ability so users can see multiple lines for this editor. Otherwise I do like it.</p>",
                "organisation": {
                    "id": 1,
                    "name": "No Organisation",
                    "website": "https://nearbeach.org",
                    "email": "noreply@nearbeach.org",
                    "profile_picture_path": null,
                    "customers": [],
                    "potential_customers": [],
                },
                "status": {
                    "id": 4,
                    "status": "In Progress",
                    "higher_order_status": {
                        "value": "Normal",
                        "label": "Normal"
                    }
                },
                "priority": {
                    "value": 1,
                    "label": "High"
                },
                "start_date": "",
                "end_date": "",
            },
            {
                "id": 1,
                "title": "Test 2",
                "description": "<p>Adding in some rich text into here. The next thing we should do is implement the ability so users can see multiple lines for this editor. Otherwise I do like it.</p>",
                "organisation": {
                    "id": 1,
                    "name": "No Organisation",
                    "website": "https://nearbeach.org",
                    "email": "noreply@nearbeach.org",
                    "profile_picture_path": null,
                    "customers": [],
                    "potential_customers": [],
                },
                "status": {
                    "id": 4,
                    "status": "In Progress",
                    "higher_order_status": {
                        "value": "Normal",
                        "label": "Normal"
                    }
                },
                "priority": {
                    "value": 1,
                    "label": "High"
                },
                "start_date": "",
                "end_date": "",
            }
        ];

        const wrapper = mount(SearchResults, {
            global: {
                plugins: [router, i18n],
            },
        });

        await flushPromises();

        const searchCards = wrapper.findAllComponents({name: "SearchCard"});
        expect(searchCards.length).toBe(2);
    });

    test("passes correct props to SearchCard components", async () => {
        const store = useSearchStore();
        store.searchResults = [
            {
                "id": 1,
                "title": "Test 1",
                "description": "<p>Adding in some rich text into here. The next thing we should do is implement the ability so users can see multiple lines for this editor. Otherwise I do like it.</p>",
                "organisation": {
                    "id": 1,
                    "name": "No Organisation",
                    "website": "https://nearbeach.org",
                    "email": "noreply@nearbeach.org",
                    "profile_picture_path": null,
                    "customers": [],
                    "potential_customers": [],
                },
                "status": {
                    "id": 4,
                    "status": "In Progress",
                    "higher_order_status": {
                        "value": "Normal",
                        "label": "Normal"
                    }
                },
                "priority": {
                    "value": 1,
                    "label": "High"
                },
                "start_date": "",
                "end_date": "",
            },
        ];

        const wrapper = mount(SearchResults, {
            global: {
                plugins: [router, i18n],
            },
        });

        await flushPromises();

        const searchCard = wrapper.findComponent({name: "SearchCard"});
        expect(searchCard.props()).toEqual({
            id: 1,
            higherOrderStatus: "high",
            objectType: "test-destination",
            status: "active",
            title: "Test 1",
        });
    });
});
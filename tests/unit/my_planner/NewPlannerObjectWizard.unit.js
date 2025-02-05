// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ParentModules from "/src/js/components/my_planner/NewPlannerObjectWizard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' NewPlannerObjectWizard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ParentModules, {
        props: {
            dateArray: [
                {
                    "_custom": {
                        "type": "reactive",
                        "objectType": "Reactive",
                        "value": {
                            "date": "2025-02-05",
                            "day": "Wednesday",
                            "data": [
                                {
                                    "user_job_id": 18,
                                    "job_date": "2025-02-05",
                                    "job_sort_number": 0,
                                    "object_type": "task",
                                    "location_id": 2,
                                    "title": "Task - QA Team",
                                    "end_date": "2024-12-24T20:16:52Z",
                                    "status": "Backlog",
                                    "higher_order_status": "Backlog"
                                }
                            ]
                        }
                    }
                },
                {
                    "_custom": {
                        "type": "reactive",
                        "objectType": "Reactive",
                        "value": {
                            "date": "2025-02-06",
                            "day": "Thursday",
                            "data": [
                                {
                                    "user_job_id": 17,
                                    "job_date": "2025-02-06",
                                    "job_sort_number": 1,
                                    "object_type": "task",
                                    "location_id": 9,
                                    "title": "New Task",
                                    "end_date": "2024-11-08T05:00:00Z",
                                    "status": "New Task",
                                    "higher_order_status": "Backlog"
                                },
                                {
                                    "user_job_id": 19,
                                    "job_date": "2025-02-06",
                                    "job_sort_number": 0,
                                    "object_type": "task",
                                    "location_id": 8,
                                    "title": "Upload image of a cat",
                                    "end_date": "2025-01-05T12:49:27Z",
                                    "status": "New Task",
                                    "higher_order_status": "Backlog"
                                }
                            ]
                        }
                    }
                },
                {
                    "_custom": {
                        "type": "reactive",
                        "objectType": "Reactive",
                        "value": {
                            "date": "2025-02-07",
                            "day": "Friday",
                            "data": [
                                {
                                    "user_job_id": 16,
                                    "job_date": "2025-02-07",
                                    "job_sort_number": 0,
                                    "object_type": "task",
                                    "location_id": 8,
                                    "title": "Upload image of a cat",
                                    "end_date": "2025-01-05T12:49:27Z",
                                    "status": "New Task",
                                    "higher_order_status": "Backlog"
                                }
                            ]
                        }
                    }
                },
                {
                    "_custom": {
                        "type": "reactive",
                        "objectType": "Reactive",
                        "value": {
                            "date": "2025-02-08",
                            "day": "Saturday",
                            "data": []
                        }
                    }
                },
                {
                    "_custom": {
                        "type": "reactive",
                        "objectType": "Reactive",
                        "value": {
                            "date": "2025-02-09",
                            "day": "Sunday",
                            "data": []
                        }
                    }
                },
                {
                    "_custom": {
                        "type": "reactive",
                        "objectType": "Reactive",
                        "value": {
                            "date": "2025-02-10",
                            "day": "Monday",
                            "data": []
                        }
                    }
                },
                {
                    "_custom": {
                        "type": "reactive",
                        "objectType": "Reactive",
                        "value": {
                            "date": "2025-02-11",
                            "day": "Tuesday",
                            "data": []
                        }
                    }
                }
            ]
        },
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
})
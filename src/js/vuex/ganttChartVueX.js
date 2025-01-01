import { DateTime } from "luxon";

export const moduleGantChart = {
    state: () => ({
        deltaDays: 0,
        ganttChartData: [],
        ganttStatusList: {
            requirement_item_status: [],
            project_status: [],
            task_status: [],
        },
        endDateGantt: 0,
        startDateGantt: 0,
    }),
    mutations: {
        updateGanttChart(state, payload) {
            const int_keys = ["deltaDays", "startDateGantt", "endDateGantt"];

            Object.keys(payload).forEach((key) => {
                if (int_keys.includes(key)) {
                    state[key] = parseInt(payload[key]);
                } else {
                    state[key] = payload[key];
                }
            });
        },
        updateGanttChartData(state, payload) {
            state.ganttChartData = payload.ganttChartData;
        },
        updateGanttStatusList(state, payload) {
            state.ganttStatusList = payload.ganttStatusList;
        },
    },
    actions: {
        initialiseGanttChartData: ({ commit }, payload) => { // Removed state
            // Calculate the delta
            let delta_days = Math.floor((payload.endDateGantt - payload.startDateGantt) / (1000 * 60 * 60 * 24));

            // If deltaDays == 0, we add 1
            if (delta_days === 0) delta_days = 1;

            // Convert some of the gantt data into the correct format
            const gant_chart_data = payload.ganttChartData.map((row) => {
                // Convert the dates
                const end_date = DateTime.fromISO(row.end_date);
                const start_date = DateTime.fromISO(row.start_date);

                // Mutate the row
                row.end_date = end_date.toMillis();
                row.start_date = start_date.toMillis();

                return row;
            }).sort((a, b) => {
                return a.start_date > b.start_date || a.end_date > b.end_date;
            });

            // Commit the data
            commit({
                type: "updateGanttChart",
                deltaDays: delta_days,
                ganttChartData: gant_chart_data,
                endDateGantt: payload.endDateGantt,
                startDateGantt: payload.startDateGantt,
            });
        },
        removeGanttChartSingleRow: ({ state, commit }, payload) => {
            // Simple remove that row using the id and object type
            const gantt_chart_data = state.ganttChartData.filter(row => {
                const parent_object_type = row.parent_object_type === null ? "" : row.parent_object_type;
                const parent_object_id = row.parent_object_id === "" ? 0 : row.parent_object_id;

                const condition1 = payload.objectType !== row.object_type;
                const condition2 = parseInt(payload.objectId) !== parseInt(row.object_id);
                const condition3 = payload.parentObjectType !== parent_object_type;
                const condition4 = parseInt(payload.parentObjectId) !== parseInt(parent_object_id);

                // To keep, at least one of the conditions have to be true
                return condition1 || condition2 || condition3 || condition4;
            });

            // Remove from the front end :)
            commit("updateGanttChartData", {
                ganttChartData: gantt_chart_data,
            });
        },
        updateGanttChartSingleRow: ({ state, commit }, payload) => {
            // Get the gantt chart data
            const gantt_chart_data = state.ganttChartData.slice(); // Create a copy to maintain immutability

            //Filter for the data we want to mutate and then apply mutations
            gantt_chart_data.filter(row => {
                const condition1 = parseInt(row.object_id) === payload.object_id;
                const condition2 = row.object_type === payload.object_type;

                return condition1 && condition2;
            }).forEach(row => {
                row.end_date = payload.end_date;
                row.higher_order_status = payload.higher_order_status;
                row.start_date = payload.start_date;
                row.status_id = payload.status_id;
            });

            // Update gantt chart data
            commit("updateGanttChartData", {
                ganttChartData: gantt_chart_data,
            });
        },
        updateGanttChartSingleRowsParent: ({ state, commit }, payload ) => {
            //Get the gantt chart data
            const gantt_chart_data = state.ganttChartData.slice(); // Create a copy to maintain immutability

            let parent_object_id = payload.parent_object_id;
            let parent_object_type = payload.parent_object_type;
            if (parseInt(parent_object_id) === 0) {
                parent_object_id = 0;
                parent_object_type = "";
            }

            //Filter for the data we are going to mutate and then apply mutations
            gantt_chart_data.filter(row => {
                let row_poi = row.parent_object_id;
                let row_pot = row.parent_object_type;
                if (row_poi === null || row_poi === undefined || row_poi === "") {
                    row_poi = 0;
                    row_pot = "";
                }

                //Conditions
                const condition1 = parseInt(row.object_id) === payload.object_id;
                const condition2 = row.object_type === payload.object_type;
                const condition3 = parseInt(row_poi) === parseInt(parent_object_id);
                const condition4 = row_pot === parent_object_type;

                return condition1 && condition2 && condition3 && condition4;
            }).forEach(row => {
                row.parent_object_type = payload.new_parent_object_type;
                row.parent_object_id = payload.new_parent_object_id;
            });

            //Update the gantt chart data
            commit("updateGanttChartData", {
                ganttChartData: gantt_chart_data,
            });
        },
    },
    getters: {
        getDeltaDays: (state) => {
            return state.deltaDays;
        },
        getGanttChartData: (state) => (parentObjectType, parentObjectId ) => {
            /*
            The top level objects, will have either a null or a string in the parent_object_(type|id).
            This is causing an issue where we can't guarentee if it will be a null, or a null string.
            Hence we are using an if statement here.
             */
            if (parentObjectType === null || parentObjectType === "")
            {
                return state.ganttChartData.filter(row => {
                    return row.parent_object_type === "" || row.parent_object_type === null;
                });
            }

            return state.ganttChartData.filter(row => {
                const condition1 = String(row.parent_object_type).toLowerCase() === parentObjectType;
                const condition2 = parseInt(row.parent_object_id) === parseInt(parentObjectId);

                return condition1 && condition2;
            });
        },
        getGanttChartDataByObject: (state) => (object_id, object_type) => {
            return state.ganttChartData.filter(row => {
                const condition1 = parseInt(row.object_id) === parseInt(object_id);
                const condition2 = row.object_type === object_type;

                return condition1 && condition2;
            });
        },
        getGanttChartDataSingleRow: (state) => (object_id, object_type, parent_object_id, parent_object_type) => {
            if (
                parseInt(parent_object_id) === 0 ||
                parent_object_id === "" ||
                parent_object_id === null ||
                parent_object_id === undefined
            ) {
                parent_object_id = 0;
                parent_object_type = "";
            }

            //Filter for the data we need
            return state.ganttChartData.filter(row => {
                let row_poi = row.parent_object_id;
                let row_pot = row.parent_object_type;
                if (row_poi === null || row_poi === undefined || row_poi === "") {
                    row_poi = 0;
                    row_pot = "";
                }

                //Conditions
                const condition1 = parseInt(row.object_id) === object_id;
                const condition2 = row.object_type === object_type;
                const condition3 = parseInt(row_poi) === parseInt(parent_object_id);
                const condition4 = row_pot === parent_object_type;

                return condition1 && condition2 && condition3 && condition4;
            })[0];
        },
        getGanttStatusList: (state) => (object_type) => {
            return state.ganttStatusList[object_type];
        },
        getEndDateGantt: (state) => {
            return state.endDateGantt;
        },
        getStartDateGantt: (state) => {
            return state.startDateGantt;
        },
    },
};

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
                const condition1 = payload.objectType !== row.object_type;
                const condition2 = parseInt(payload.objectId) !== parseInt(row.object_id);

                // To keep, at least one of the conditions have to be true
                return condition1 || condition2;
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
        updateGanttChartSingleRowsParent: ({ state, commit }, payload ) => {},
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
        getGanttChartDataSingleRow: (state) => (index) => {
            return state.ganttChartData[index];
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

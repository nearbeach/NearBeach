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

            // Mutate the gantt chart data
            gantt_chart_data[payload.index] = payload.value;

            // Update gantt chart data
            commit("updateGanttChartData", {
                ganttChartData: gantt_chart_data,
            });
        },
    },
    getters: {
        getDeltaDays: (state) => {
            return state.deltaDays;
        },
        getGanttChartData: (state) => {
            return state.ganttChartData;
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

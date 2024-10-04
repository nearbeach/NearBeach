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
			// Defining int keys
			const int_keys = ["deltaDays", "startDateGantt", "endDateGantt"];

			// Loop through the payload and update the state
			Object.keys(payload).forEach((key) => {
				state[key] = int_keys.includes(key)
					? parseInt(payload[key])
					: payload[key];
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
		initialiseGanttChartData: ({ commit }, payload) => {
			// Removed state
			// Calculate the delta days
			let delta_days = Math.floor(
				(payload.endDateGantt - payload.startDateGantt) /
					(1000 * 60 * 60 * 24)
			);
			if (delta_days === 0) delta_days = 1;

			// Convert the Gantt chart data into the correct format
			const gant_chart_data = payload.ganttChartData.map((row) => ({
				...row,
				end_date: DateTime.fromISO(row.end_date).toMillis(),
				start_date: DateTime.fromISO(row.start_date).toMillis(),
			}));

			// Commit the updated data
			commit({
				type: "updateGanttChart",
				deltaDays: delta_days,
				ganttChartData: gant_chart_data,
				endDateGantt: payload.endDateGantt,
				startDateGantt: payload.startDateGantt,
			});
		},
		removeGanttChartSingleRow: ({ commit }, payload) => {
			// Removed state
			// Remove the row using the id and object type
			const gantt_chart_data = state.ganttChartData.filter(
				(row) =>
					payload.objectType !== row.object_type ||
					parseInt(payload.objectId) !== parseInt(row.object_id)
			);

			// Commit the updated data
			commit("updateGanttChartData", {
				ganttChartData: gantt_chart_data,
			});
		},
		updateGanttChartSingleRow: ({ commit }, payload) => {
			// Removed state
			// Update the Gantt chart data for a single row
			const gantt_chart_data = [...state.ganttChartData];
			gantt_chart_data[payload.index] = payload.value;

			// Commit the updated data
			commit("updateGanttChartData", {
				ganttChartData: gantt_chart_data,
			});
		},
	},
	getters: {
		getDeltaDays: (state) => state.deltaDays,
		getGanttChartData: (state) => state.ganttChartData,
		getGanttChartDataSingleRow: (state) => (index) =>
			state.ganttChartData[index],
		getGanttStatusList: (state) => (object_type) =>
			state.ganttStatusList[object_type],
		getEndDateGantt: (state) => state.endDateGantt,
		getStartDateGantt: (state) => state.startDateGantt,
	},
};

export const moduleGantChart = {
    state: () => ({
        deltaDays: 0,
        ganttChartData: [],
        endDateGantt: 0,
        startDateGantt: 0,
    }),
    mutations: {
        updateGanttChart(state, payload) {
            //Defining int keys
            const int_keys = ["deltaDays", "startDateGantt", "endDateGantt"];

            //Loop through the payload and update the results according to the keys
            Object.keys(payload).forEach((key) => {
                //Update the results
                if (int_keys.includes(key)) {
                    state[key] = parseInt(payload[key]);
                } else {
                    state[key] = payload[key];
                }
            });
        },
    },
    actions: {
        initialiseGanttChartData: ({state, commit}, payload) => {
            //Calculate the delta
            let delta_days =  Math.floor((payload.endDateGantt - payload.startDateGantt) / (1000 * 60 * 60 * 24));

            //If deltaDays == 0, we add 1
            if (delta_days === 0) delta_days = 1;

            //Commit the data
            commit({
                type: "updateGanttChart",
                deltaDays: delta_days,
                ganttChartData: payload.ganttChartData,
                endDateGantt: payload.endDateGantt,
                startDateGantt: payload.startDateGantt,
            });
        },
    },
    getters: {},
}
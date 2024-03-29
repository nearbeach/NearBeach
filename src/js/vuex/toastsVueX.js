export const moduleToasts = {
    state: () => ({
        toastList: [],
    }),
    mutations: {
        updateToastList(state, payload) {
            state.toastList = payload.toastList;
        }
    },
    actions: {
        newToast({commit, state}, payload) {
            //Grab the current timestamp
            const timestamp = new Date();

            //Setup new toast object with default values
            let new_toast = {
                delay: 20000,
                extra_classes: "",
                header: "",
                message: "",
                timestamp: timestamp.getTime(),
                unique_type: "",
                unique_uuid: crypto.randomUUID(),
            };

            //Loop through each keys for the payload, and update the relevant field
            const continue_keys = ["type"];
            Object.keys(payload).forEach((key) => {
                //Skip some certain keys
                if (continue_keys.includes(key)) {
                    return;
                }

                //Update the results
                new_toast[key] = payload[key];
            });

            //Grab a snapshot of the current state
            let update_state = state.toastList;

            //Filter out any expired toasts
            update_state = update_state.filter((row) => {
                //Keep if delay === 0
                const condition_1 = row.delay === 0;

                //Keep if current_timestamp <= toast_timestamp + delay
                const condition_2 = timestamp.getTime() <= row.timestamp + row.delay;

                //OR conditioning
                return condition_1 || condition_2;
            });

            //Filter out - any toasts that has the same unique type (exclude empty unique types)
            if (new_toast.unique_type !== "") {
                //There is a non empty type, filter out any types that match
                update_state = update_state.filter((row) => {
                    return row.unique_type !== new_toast.unique_type;
                })
            }

            //Append the new toast
            update_state.push(new_toast);

            //Update the state appropriately
            commit({
                type: "updateToastList",
                toastList: update_state,
            });
        },
        removeToast({commit, state}, payload) {
            //Create the new data set
            const update_state = state.toastList.filter((row) => {
                return row.unique_uuid !== payload.unique_uuid;
            });

            //Update the state appropriately
            commit({
                type: "updateToastList",
                toastList: update_state,
            });
        }
    },
    getters: {
        getToastList: (state) => {
            return state.toastList;
        },
    },
}
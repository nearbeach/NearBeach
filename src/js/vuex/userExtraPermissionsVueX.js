export const moduleUserExtraPermissions = {
    state: () => ({
        userExtraPermissions: [],
    }),
    mutations: {
        updateUserExtraPermissions(state, payload) {
            state.userExtraPermissions = payload.userExtraPermissions;
        },
    },
    action: {},
    getters: {
        getUserExtraPermission: (state) => (extraPermission) => {
            //Filter the state for that object_type
            //AND filter for the object permission value for being 1 (true)
            const filtered = state.userExtraPermissions.filter((row) => {
                const condition_1 = row.object_type.toLowerCase() === extraPermission.toLowerCase();
                const condition_2 = parseInt(row.object_permission_value) === 1;

                return condition_1 && condition_2;
            });

            //If there are any rows left, it means the user has permission for this particular extra permission
            return filtered.length > 0;
        }
    },
}
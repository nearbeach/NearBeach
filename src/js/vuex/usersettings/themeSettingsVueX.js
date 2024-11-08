export const themeSettings = {
    state: () => ({
        contentCss: "default",
        skin: "oxide",
        theme: "light",
    }),
    mutations: {
        updateThemeSettings(state, payload) {
            state.contentCss = payload.contentCss;
            state.skin = payload.skin;
            state.theme = payload.theme;
        },
        // updateTheme(state, payload) {
        //     state.theme = payload.theme;
        // },
    },
    actions: {
        processThemeUpdate({commit}, payload) {
            //Depending on the theme, depends on the values
            switch (payload.theme) {
                case "dark":
                    commit("updateThemeSettings", {
                        contentCss: "dark",
                        skin: "oxide-dark",
                        theme: "dark",
                    });
                    break;
                default:
                    commit("updateThemeSettings", {
                        contentCss: "default",
                        skin: "oxide",
                        theme: "light",
                    });
            }
        }
    },
    getters: {
        getContentCss: (state) => {
            return state.contentCss;
        },
        getSkin: (state) => {
            return state.skin;
        },
        getTheme: (state) => {
            return state.theme;
        },
    },
}
import {darkTheme} from "naive-ui";

export default {
    data() {
        return {
            darkTheme: darkTheme,
        }
    },
    methods: {
        getTheme(theme) {
            //Depending on the theme depends what we send back
            switch (theme) {
                case "dark":
                    return darkTheme;
                default:
                    return null;
            }
        }
    }
}
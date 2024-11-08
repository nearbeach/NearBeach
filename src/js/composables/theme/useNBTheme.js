import { toValue } from "vue";
import { darkTheme } from "naive-ui";

export function useNBTheme(theme) {
    const value = toValue(theme);

    //Depending on the theme depends what we send back
    switch (value) {
        case "dark":
            return darkTheme;
        default:
            return null;
    }
}
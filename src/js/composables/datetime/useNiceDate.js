import { DateTime } from "luxon";
import { toValue } from "vue";

export function useNiceDate(input_date) {
    const value = toValue(input_date);

    //If input_date is null or empty string - return empty string
    if (value === "" || value === null || value === undefined) {
        return "";
    }
    //Use Luxon to convert the date nicely
    const new_date = DateTime.fromISO(value);

    //Return the nice outputted date
    return new_date.toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY);
}
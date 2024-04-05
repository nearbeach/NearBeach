import {DateTime} from "luxon";

export default {
    methods: {
        getNiceDatetime(input_date) {
            //If input_date is null or empty string - return empty string
            if (input_date === "" || input_date === null || input_date === undefined) {
                return "";
            }
            //Use Luxon to convert the date nicely
            const new_date = DateTime.fromISO(input_date);

            //Return the nice outputted date
            return new_date.toLocaleString(DateTime.DATETIME_MED);
        },
        getNiceDatetimeFromInt(input_date) {
            //If input_date is null or empty string - return empty string
            if (input_date === "" || input_date === null || input_date === undefined) {
                return "";
            }
            //Use Luxon to convert the date nicely
            const new_date = DateTime.fromMillis(input_date);

            //Return the nice outputted date
            return new_date.toLocaleString(DateTime.DATETIME_MED);
        },
        getNiceDate(input_date) {
            //If input_date is null or empty string - return empty string
            if (input_date === "" || input_date === null || input_date === undefined) {
                return "";
            }
            //Use Luxon to convert the date nicely
            const new_date = DateTime.fromISO(input_date);

            //Return the nice outputted date
            return new_date.toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY);
        },
        disableDate(timeStamp) {
            //Get date but level the time to 00:00:00
            const date = new Date();
            date.setMilliseconds(0);
            date.setSeconds(0);
            date.setHours(0);

            //Return anything that is less than a day ago.
            return timeStamp <= date.getTime() - 3600000;
        },
    },
};

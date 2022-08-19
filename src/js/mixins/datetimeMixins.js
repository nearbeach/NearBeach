import {DateTime} from "luxon";

export default {
    methods: {
        getNiceDate: function(input_date) {
            //Use Luxon to convert the date nicely
            let new_date = DateTime.fromISO(input_date);

            //Return the nice outputted date
            return new_date.toLocaleString(DateTime.DATETIME_MED);
        },
    }
}
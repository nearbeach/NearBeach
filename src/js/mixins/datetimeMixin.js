import { DateTime } from "luxon";

export default {
	methods: {
		getNiceDate: function (input_date) {
			//Use Luxon to convert the date nicely
			const new_date = DateTime.fromISO(input_date);

			//Return the nice outputted date
			return new_date.toLocaleString(DateTime.DATETIME_MED);
		},
		disableDate: function (timeStamp) {
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

function check_end_date() {
	/* Method
	 * ~~~~~~
	 * 1.) Obtain all element values
	 * 2.) Check to see if the date is actually a date
	 * 3.) (not programmed yet) Edit the day element by removing any days
	 * that are not associated with the choosen month.
	 */
	var year_element = document.getElementById("id_finish_date_year");
	var month_element = document.getElementById("id_finish_date_month");
	var day_element = document.getElementById("id_finish_date_day");
	
	fix_dates(year_element, month_element, day_element);
}


function check_start_date() {
	/* Method
	 * ~~~~~~
	 * 1.) Obtain all element values
	 * 2.) Check to see if the date is actually a date
	 * 3.) (not programmed yet) Edit the day element by removing any days
	 * that are not associated with the choosen month.
	 */
	var year_element = document.getElementById("id_start_date_year");
	var month_element = document.getElementById("id_start_date_month");
	var day_element = document.getElementById("id_start_date_day");

	fix_dates(year_element, month_element, day_element);
}


function fix_dates(year_element, month_element, day_element) {
	/* First we check Feb.
	 * 
	 * Method
	 * ~~~~~~
	 * 1.) Check to see if the year is a leap year using the following;
	 * -- default = 28
	 * -- year / 4.0 = year / 4 = 29
	 * -- year / 100.0 = year / 100 = 28
	 * -- year / 1000.0 = year / 1000 = 29
	 * 2.) If date_element.value > max_days, change value to max_days
	 */
	 if (month_element.value == 2) {
		max_day = 28;
		
		//Hide/Unhide the unrequired dates
		day_element[28].hidden = true; //29th
		day_element[29].hidden = true; //30th
		day_element[30].hidden = true; //31th
		
		// If the year can be divided by 4 cleanly, it is a leap year
		if (parseInt(year_element.value/4) == parseInt(year_element.value)/4.0) {
			max_day = 29;
			day_element[28].hidden = false; //29th
		}
		
		// Exception is on the centruary year, is not a leap year
		if (parseInt(year_element.value/100) == parseInt(year_element.value)/100.0) {
			max_day = 28;
		}
		
		// Unless it falls on a millenium year
		if (parseInt(year_element.value/1000) == parseInt(year_element.value)/1000.0) {
			max_day = 29;
			day_element[28].hidden = false; //29th
		}
		
		// nwo check to see if the day value exceeds the max value
		if (day_element.value > max_day) {
			day_element.value = max_day;
		}


	/* else if the months are;
	 * April - 4th month
	 * June - 6th month
	 * September - 9th month
	 * November - 11th month
	 * Then only 30 days
	 */		
	} else if ((month_element.value == 4) ||
		(month_element.value == 6) ||
		(month_element.value == 9) ||
		(month_element.value == 11)) {
		if (day_element.value > 30) {
				day_element.value = 30;
			}
		
		//Hide/Unhide the unrequired dates
		day_element[28].hidden = false; //29th
		day_element[29].hidden = false; //30th
		day_element[30].hidden = true; //31th
	} else {
		//The rest of the months have 31 days
		//Hide/Unhide the unrequired dates
		day_element[28].hidden = false; //29th
		day_element[29].hidden = false; //30th
		day_element[30].hidden = false; //31th
	}	
} 


function initiate_dates() {
	check_start_date();
	check_end_date();
}

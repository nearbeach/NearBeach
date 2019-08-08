function timesheet_setup() {
    /* This function will finish setting up the timesheet - i.e. setup the datetime functions*/
    $( "#id_timesheet_date" ).datepicker({
        dateFormat: "yy-mm-dd"
    });

    $("#id_timesheet_start_time").timepicker({
        'scrollDefault': 'now',
    });

    $("#id_timesheet_end_time").timepicker({
        'scrollDefault': 'now',
    });
}
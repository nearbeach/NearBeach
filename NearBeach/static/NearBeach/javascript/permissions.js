function set_permissions(user_permission_level) {
    /*
    If the user permission level is 1 or less, place everything
    into read only mode. Remove all BUTTONS
     */
    if (user_permission_level <= 1) {
        //Disable all the input fields
        $("input").prop("readonly", true);

        //Disable all the select statements
        $("select").prop("disabled", true);

        //Disable all text area
        $("textarea").prop("disabled", true);

        //Disable all the buttons.
        $("input[type=submit]").prop("disabled", true);
    }

}


function set_project_history(project_history_permission) {
    /*
    If a read only user has the ability to add in history for project history, then we
    might as well turn it on.
     */
    if (project_history_permission > 0) {
        //The user has permission
        $("#id_project_history").prop("disbaled", false);
        $("#project_history_submit").prop("disbaled", false);
    }

}
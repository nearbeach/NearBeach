/*
The following script will be used to interact with the error modal.
 */

function new_error(error_string) {
    //Show the modal
    $("#error_modal").modal({
        show: true,
        keyboard: true,
        focus: true,
    });

    //Add the error to the current modal
    $("#error_modal_body").append(`<hr>${error_string}`);
}
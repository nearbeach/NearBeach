

function add_bug(location_id, destination,bug_id, bug_client_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#id_"+bug_id+"_"+bug_client_id).html("Adding...");


    $.ajax({
        url: '/bug_add/' + location_id + '/' + destination + '/' + bug_id + '/' + bug_client_id + '/',
        data: {},
        type: 'POST',
        success: function(data) {
            //$(this).html("Added");
            load_bug_list();
            $("#id_"+bug_id+"_"+bug_client_id).html("Added");
        },
        error: function() {
            alert("We are sorry, we experienced an error trying to add your bug to the " + destination);
        },
    });
}
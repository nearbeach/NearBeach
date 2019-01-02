function assigned_user_delete(user_id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/assigned_user_delete/' + user_id + '/',
        data: {},
        datatype: 'HTML',
        type: 'POST',
        success: function(data) {
            //Reload assigned users
            load_assigned_user_list();
            load_assigned_user_add();
        },
        error: function() {
            alert("Sorry, but deleting the assigned user did not work");
        }
    })
}
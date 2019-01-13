function confirm_delete_document(document_key,location_id,destination,folder_id) {
    //bring up modal
    //wait 2 seconds
    //enable button

    $("#confirm_document_delete").modal("show");

    //$(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
    if ((folder_id == null) || (folder_id == 0)) {
        $("#remove_document_confirmed").attr('onclick','delete_document("' + document_key + '","' + location_id + '","' + destination + '")');
    } else {
        $("#remove_document_confirmed").attr('onclick','delete_document("' + document_key + '","' + location_id + '","' + destination + '","' + folder_id + '")');
    }


    setTimeout(function () {
        document.getElementById("remove_document_confirmed").disabled = false;
    }, 2000);
}


function confirm_delete_folder(folder_id,location_id,destination,current_folder_id) {
    //Show the modal - confirm that the user wants to delete the folder
    $("#confirm_folder_delete").modal("show");

    //We need to pass on the information of where to go when the delete button is clicked
    if ((current_folder_id == null) || (current_folder_id == 0)) {
        $("#remove_folder_confirmed").attr('onclick','delete_folder(' + folder_id + ',' + location_id + ',"' + destination + '")');
    } else {
        $("#remove_folder_confirmed").attr('onclick','delete_folder(' + folder_id + ',' + location_id + ',"' + destination + '",' + current_folder_id + ')');
    }

    //We want to make sure the delete button is disabled for 2 seconds
    setTimeout(function () {
        document.getElementById("remove_folder_confirmed").disabled = false;
    }, 2000);
}


function delete_document(document_key,location_id,destination,folder_id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/delete_document/' + document_key + '/',
        data: {},
        dataType: "HTML",
        type: "POST",
        success: function(data) {
            $("#confirm_document_delete").modal("hide"); //Remove the modal
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            alert("Sorry, there was an issue deletng the file");
        }

    })
}


function delete_folder(folder_id,location_id,destination,current_folder_id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/delete_folder/' + folder_id + '/',
        data: {},
        dataType: "HTML",
        type: "POST",
        success: function(data) {
            $("#confirm_folder_delete").modal("hide"); //Remove the modal
            if ((current_folder_id == null) || (current_folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, current_folder_id);
            }
        },
        error: function() {
            alert("Sorry - could not remove folder");
        }

    })
}


function load_document_tree_list(location_id, destination, folder_id) {
    /*
    The URL changes depending on the folder_id. If the folder_id is defined then we want to include it -
    otherwise we do not.
     */
    if (folder_id == null) {
        var url = '/document_tree_list/' + location_id + '/' + destination + '/';
    } else {
        var url = '/document_tree_list/' + location_id + '/' + destination + '/' + folder_id + '/';
    }
    //Load Project History
    $.ajax({
        url: url,
        data: {},
        dataType: 'HTML',
        type: 'GET',
        success: function(data) {
            $('#document_tree_list').html(data);
        },
        error: function() {
            $('#document_tree_list').html('<h2>Document Tree</h2>Sorry, document tree encounted an error and did not load.');
        }
    });
};


function new_folder(location_id,destination,folder_id) {
    console.debug("Sending in new folder information");
//Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Get form data
    var form_data = new FormData($('#new_folder_form')[0]);

    $.ajax({
        url: '/document_tree_folder/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#new_folder_modal").modal("hide"); //Remove the modal
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });
}


function upload_document(location_id,destination,folder_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    //Get form data
    var form_data = new FormData($('#document_upload_form')[0]);

    $.ajax({
        xhr: function() {
            var xhr = new window.XMLHttpRequest();

            // Upload progress
            xhr.upload.addEventListener("progress", function(evt){
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    //Do something with upload progress
                    $("#document_upload_progress").css(
                        'width', percentComplete * 100 + '%'
                    );
                }
           }, false);
           return xhr;
        },

        url: '/document_tree_upload/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            $("#document_upload_progress").css('width','0%;');
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });
}


function upload_url(location_id, destination, folder_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Get form data
    var form_data = new FormData($('#document_url_form')[0]);

    $.ajax({
        url: '/document_tree_url/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#new_url_modal").modal("hide"); //Remove the modal
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });


}


/*
The following code should be inputted into the object you wish to add document list to.

<h2>Document Uploads</h2>
<div class="document_tree_list" id="document_tree_list">
    <h2>Document Tree List</h2>
    Loading...
</div>
 */

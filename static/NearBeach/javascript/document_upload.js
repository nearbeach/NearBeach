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


/*
The following code should be inputted into the object you wish to add document list to.

<h2>Document Uploads</h2>
<div class="document_tree_list" id="document_tree_list">
    <h2>Document Tree List</h2>
    Loading...
</div>
 */

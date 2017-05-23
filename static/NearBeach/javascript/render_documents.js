function render_folders(document_folders_results, current_folder) {
	/*
	Render folders function renders each folder. It is a recursive function.
	Each folder it will render it will give an id of the folder number with
	the suffix _folder
	i.e 1_folder

	Step 1
	~~~~~~
	We currently only want the folders for the current location.
	 */
	var folder_results = document_folders_results.filter(function(i, n) {
		return (i.fields.parent_folder_id == current_folder);
	});
	/*
	Step 2
	~~~~~~
	We will loop through each of the folder resules. Make sure that there are
	no sub folders. If there are any sub folders we will call this function
	recursovly with the sub folder information.
	 */
	var content_string = '';
	for (var i=0; i<folder_results.length; i++) {
		content_string += '<div class="folder_content"><div class=""folder_header"><b>';
		content_string += '<img src="/static/NearBeach/images/folder-icon-small.png" height="20px"> ';
		content_string += folder_results[i].fields.document_folder_description;
		content_string += '</b></div><div class="folder_sub_content" id="'+ folder_results[i].pk + '_folder">';

		content_string += render_folders(document_folders_results, folder_results[i].pk);
		content_string += '</div>';
	}
	return content_string;

}

function render_documents(document_results, site_url) {
	for (var i=0; i<document_results.length; i++) {
		var content_string = '<a href="';
		if ((document_results[i].fields.document == '') || (document_results[i].fields.document == null)) {
            content_string += document_results[i].fields.document_url_location;

        } else {
			content_string += site_url + document_results[i].fields.document;
		}
		content_string += '" target="_blank">';
		content_string += document_results[i].fields.document_description;
		content_string += '</a>';


		if (document_results[i].fields.document_folder_id == null) {
			destination_folder = document.getElementById("root_folder");
		} else {
			destination_folder = document.getElementById(document_results[i].fields.document_folder_id + "_folder");
		}
		destination_folder.innerHTML = destination_folder.innerHTML + '<br/>' + content_string;
	}
}

function upload_or_link() {
    overlay_upload = document.getElementById("overlay_upload");
    overlay_link = document.getElementById("overlay_link");
    upload_type = document.getElementById("upload_type");


    if (upload_type.selectedIndex == 0) {
        overlay_upload.style.display = "block";
        overlay_link.style.display = "none";
    } else {
        overlay_upload.style.display = "none";
        overlay_link.style.display = "block";
    }

    //Check to make sure if submit needs to be enabled
    enable_submit()
}

function enable_submit() {
	upload_type = document.getElementById("upload_type");


	id_document = document.getElementById("id_document");
	id_document_url_location = id_document_url_location.getElementById("id_document_url_location");
	id_document_description = document.getElementById("id_document_description");

}

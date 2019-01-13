function render_folders(document_folders_results, current_folder) {
	/*
	Render folder function renders each folder. It is a recursive function.
	Each folder it will render it will give an id of the folder number with
	the suffix _folder
	i.e 1_folder

	Step 1
	~~~~~~
	We currently only want the folder for the current location.
	 */
	var folder_results = document_folders_results.filter(function(i, n) {
		return (i.fields.parent_folder_id == current_folder);
	});
	/*
	Step 2
	~~~~~~
	We will loop through each of the folder resules. Make sure that there are
	no sub folder. If there are any sub folder we will call this function
	recursovly with the sub folder information.
	 */
	var content_string = '';
	for (var i=0; i<folder_results.length; i++) {
		content_string += '<li><label>' + folder_results[i].fields.folder_description + '</label>';
		content_string += '<input type="checkbox" id="' + folder_results[i].pk + '_checkbox">';
		content_string += '<ul id="' + folder_results[i].pk + '_folder">';
		content_string += render_folders(document_folders_results, folder_results[i].pk);
		content_string += '</ul></li>';

		/*
		Minor step
		~~~~~~~~~~
		We are now adding the folder to the new_document_location select
		*/
		var new_document_location = document.getElementById("parent_folder_id");
		var folder_location = document.getElementById("folder_location");
		var opt = document.createElement('option');
		opt.value = folder_results[i].pk;
		opt.innerHTML = folder_results[i].fields.folder_description;
		new_document_location.appendChild(opt);
		//folder_location.appendChild(opt);

		//Ok, I am cheating here.
		//Bug with JAVASCRIPT - will now allow me to append the same opt twice.
		var folder_location = document.getElementById("folder_location");
		var opt2 = document.createElement('option');
		opt2.value = folder_results[i].pk;
		opt2.innerHTML = folder_results[i].fields.folder_description;
		folder_location.appendChild(opt2);

	}
	return content_string;

}

function add_new_document() {
	new_document_dialog = document.getElementById("overlay_new_document");
	new_document_dialog.style.visibility = (new_document_dialog.style.visibility == "visible") ? "hidden" : "visible";
}

function add_new_folder() {
    new_folder_dialog = document.getElementById("overlay_new_folder");
    new_folder_dialog.style.visibility = (new_folder_dialog.style.visibility == "visible") ? "hidden" : "visible";
}

function render_documents(document_results, site_url) {
	for (var i=0; i<document_results.length; i++) {
		var content_string = '<a href="';
		if ((document_results[i][3] == '') || (document_results[i][3] == null)) {
            content_string += document_results[i][2];

        } else {
			content_string += site_url + document_results[i][3];
		}
		content_string += '" target="_blank">';
		content_string += document_results[i][1];
		content_string += '</a>';

		if ((document_results[i][4] == null) || (document_results[i][4] == "")) {
			destination_folder = document.getElementById("root_folder");
		} else {
			destination_folder = document.getElementById(document_results[i][4] + "_folder");
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
	/*
	So I didn't like the spaghetti if statements left here. So I invented this simple
	boolean way to disable and enable the submit button.

	It works by checking to see if there are values in the required fields. It will
	activate the button if either one of the two conditions is met. Simple.
	 */
	id_document = Boolean(document.getElementById("id_document").value != "");
	id_document_url_location = Boolean(document.getElementById("id_document_url_location").value != "");
	id_document_description = Boolean(document.getElementById("id_document_description").value != "");
	id_new_folder = Boolean(document.getElementById("id_folder_description").value == "");

	new_document = document.getElementById("new_document");
	new_folder = document.getElementById("new_folder");
	new_document.disabled = !Boolean((id_document && id_document_description) || (id_document_url_location && id_document_description));
	new_folder.disabled = id_new_folder;
}

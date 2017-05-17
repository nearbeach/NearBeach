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

function render_documents(document_folders_results, current_folder) {

}
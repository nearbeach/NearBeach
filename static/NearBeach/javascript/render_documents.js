function render_documents(document_folders_results, documents_results, current_folder) {
	//alert(current_folder);
	content_string = '';
	var folder_results = document_folders_results.filter(function(i, n) {
		return (i.fields.parent_folder_id == current_folder);
	});

	var doc_results = documents_results.filter(function(i, n) {
			return (i.fields.document_folder_id == current_folder);
	});
	//alert(folder_results);

	for (var i=0; i<folder_results.length; i++) {
		content_string += '<div class="folder_content"><div class="folder_header"><b>'
		content_string += folder_results[i].fields.document_folder_description
		content_string += '</b></div><div class="folder_sub_content">'

		content_string += render_documents(document_folders_results, documents_results, folder_results[i].pk)


		for (var j=0; j<doc_results.length; j++) {
			content_string += '<div>-- '
			content_string += doc_results[j].fields.document_description
			content_string += '</div>'
		}

		content_string += '</div></div>'
	}

	return content_string
}
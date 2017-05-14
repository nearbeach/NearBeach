function render_documents(document_folders_results, documents_results, current_folder) {
	//alert(current_folder);
	content_string = '';
	var folder_results = document_folders_results.filter(function(i, n) {
		return (i.fields.parent_folder_id == current_folder);
	});


	//alert(folder_results);

	for (var i=0; i<folder_results.length; i++) {
		var doc_results = documents_results.filter(function(i, n) {
			return (i.fields.document_folder_id == current_folder);
	    });

		content_string += '<div class="folder_content"><div class="folder_header"><b>';
		content_string += '<img src="/static/NearBeach/images/folder-icon-small.png" height="20px"> ';
		content_string += folder_results[i].fields.document_folder_description;
		content_string += '</b></div><div class="folder_sub_content">';

		content_string += render_documents(document_folders_results, documents_results, folder_results[i].pk);
		content_string += '</div>';


		for (var j=0; j<doc_results.length; j++) {
            content_string += '<div>-- ';

            if (doc_results[j].fields.document) {
                //The document has been uploaded
                content_string += "<a href='";
                content_string += doc_results[j].fields.document;
                content_string += "' target='_blank'>";
            } else {
			    content_string += "<a href='";
			    content_string += doc_results[j].fields.document_url_location;
			    content_string += "' target='_blank'>";
			}
			content_string += doc_results[j].fields.document_description
			content_string += "</a></div>";
		}

		content_string += '</div>'
	}

	return content_string
}
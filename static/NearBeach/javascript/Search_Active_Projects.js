function Search_Active_Projects() {
	//Varables used in the function
	var input, filter, table, tr, column_project, column_task, column_description, i;
	
	//Get the value from the search box
	input = document.getElementById("Search_Active_Projects");
	
	//We want to compare apples with apples, make all uppercase
	filter = input.value.toUpperCase();

	//Get reference to the table
	table = document.getElementById("Active_Projects_Table");

	//Separate the table into it's separate elements
	tr = table.getElementsByTagName("tr");

	//The loop will go through and check the filter against each value
	//Any row that does not contain the filter value it will hide
	//by using the display = 'none'
	for (i = 0; i < tr.length; i++) {
		column_project = tr[i].getElementsByTagName("td")[0];
		column_task = tr[i].getElementsByTagName("td")[1];
		column_description = tr[i].getElementsByTagName("td")[2];
		if (column_project || column_task || column_description) {
			if (column_project.innerHTML.toUpperCase().indexOf(filter) > -1 ||
				column_task.innerHTML.toUpperCase().indexOf(filter) > -1 ||
				column_description.innerHTML.toUpperCase().indexOf(filter) > -1	) {
				tr[i].style.display = "";
			} else {
				tr[i].style.display = "none";
			}
		}
	}
}


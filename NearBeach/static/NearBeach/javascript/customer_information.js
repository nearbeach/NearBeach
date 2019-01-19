function enable_disable_add_campus() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to 
	 * re-enable it again.
	 */
	var id_add_cammpus_select = document.getElementById("id_add_cammpus_select");
	var id_add_cammpus_submit = document.getElementById("id_add_cammpus_submit");
	
	if (id_add_cammpus_select.selectedIndex==0) {
		id_add_cammpus_submit.disabled = true;
	} else {
		id_add_cammpus_submit.disabled = false;
	}
}

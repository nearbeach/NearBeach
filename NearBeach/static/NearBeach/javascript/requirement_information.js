function enable_disable_add_customer() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to
	 * re-enable it again.
	 */
	var add_customer_select = document.getElementById("add_customer_select");
	var add_customer_submit = document.getElementById("add_customer_submit");

	if (add_customer_select.selectedIndex==0) {
		add_customer_submit.disabled = true;
	} else {
		add_customer_submit.disabled = false;
	}
}
//Functions
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

function enable_disable_add_user() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to
	 * re-enable it again.
	 */
	var add_user_select = document.getElementById("add_user_select");
	var add_user_submit = document.getElementById("add_user_submit");

	if (add_user_select.selectedIndex==0) {
		add_user_submit.disabled = true;
	} else {
		add_user_submit.disabled = false;
	}
}


function enable_disable_add_cost() {
	var cost_description = document.getElementById("id_cost_description");
	var cost_amount = document.getElementById("id_cost_amount");
	var add_cost_submit = document.getElementById("add_cost_submit");

	if ((cost_description.value != '') && (cost_amount.value != '')) {
		add_cost_submit.disabled = false;
	} else {
		add_cost_submit.disabled = true;
	}
}


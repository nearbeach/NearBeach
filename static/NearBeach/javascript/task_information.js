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

function running_total() {
	/*
	Method
	~~~~~~
	The running total is calculated AFTER ALL data has been created
	to help save server memory for large datasets.

	1.) Get variables and set running total = 0
	2.) LOOP
	3.) Find cost amount and add to running total
	4.) Edit running total spot
	5.) Loop
	6.) Fill out grand total
	 */
	var cost_amount = document.getElementsByName("cost_amount");
	var running_total = document.getElementsByName("running_total");
	var grand_total = document.getElementById("grand_total");
	var running_total_amount = 0;

	//The loop
	for(var i = 1; i <= running_total.length; i++) {
		running_total_amount = running_total_amount + Number(cost_amount[i].innerHTML);
		running_total[i-1].innerHTML = running_total_amount;
	}

	grand_total.innerHTML = running_total_amount;
}
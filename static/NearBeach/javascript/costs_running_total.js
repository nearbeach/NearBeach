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
	try {
		var cost_amount = document.getElementsByName("cost_amount");
		var running_total = document.getElementsByName("running_total");
		var grand_total = document.getElementById("grand_total");
		var running_total_amount = 0;

		//The loop
		for(var i = 1; i <= running_total.length; i++) {
			running_total_amount = running_total_amount + Number(cost_amount[i].innerHTML);
			running_total[i-1].innerHTML = running_total_amount;
		}

		if (grand_total.exists(e)) {
			grand_total.innerHTML = running_total_amount;
		}

	}
	catch(err) {
		//Nothing to do.
	}
}
function enable_disable_add_customer() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to 
	 * re-enable it again.
	 */
	var id_add_customer_select = document.getElementById("id_add_customer_select");
	var id_add_customer_submit = document.getElementById("id_add_customer_submit");

	if (id_add_customer_select.selectedIndex==0) {
		id_add_customer_submit.disabled = true;
	} else {
		id_add_customer_submit.disabled = false;
	}
}



/*
The following javascript is to fix a bug where the map only renders on the right side
of the screen. The javascript changes the position to relative. Which fixes this issue.
 */
function relayout_map() {
    //alert("WHY DO I NEED TO ADD AN ALERT?")
    var mapbox = document.getElementById("map");
    var mapbox_canvas = mapbox.getElementsByClassName("mapboxgl-canvas");

    for (var i=0; i < mapbox_canvas.length; i++) {
        mapbox_canvas[i].style.position="relative";
    }
}

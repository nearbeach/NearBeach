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

function on_page_load(country, region) {
    //Quickly, relayout the map before anyone knows
    relayout_map()

    /* Information
     * ~~~~~~~~~~~
     * The following will setup the page correctly. We want the ability for the country and region to be selected
     * correctly, and any options under the region that should not be appearing will be disabled. The disabled
     * will disappear through CSS manipulation.
     */
    var campus_country_select = document.getElementById("campus_country_id").getElementsByTagName("option");
    var campus_region_select = document.getElementById("campus_region_id").getElementsByTagName("option");


    //Select the correct country
    for (var i=0; i<campus_country_select.length; i++) {
        //Select country if it is the correct one and then break out of the loop
        if (campus_country_select[i].value.toLowerCase() == country.toLowerCase()) {
            document.getElementById("campus_country_id").selectedIndex = i;
            break;
        }
    }

    //Select the correct region, and disable all others
    for (var i=1; i<campus_region_select.length; i++) {
        //Select region if it is the correct one
        if (campus_region_select[i].text.toLowerCase() == region.toLowerCase()) {
            document.getElementById("campus_region_id").selectedIndex = i;
        }

        //Enable or disable region due to country
        var country_id = campus_region_select[i].getAttribute("country_id");
        if (country_id.toLowerCase() == country.toLowerCase()) {
            campus_region_select[i].disabled = false;
        } else {
            campus_region_select[i].disabled = true;
        }
    }


}


function country_changed() {
    var country = document.getElementById("campus_country_id").value;
    var region = document.getElementById("campus_region_id");
    var region_country = region[region.selectedIndex].getAttribute("country_id");


     //Set the region to ------
     document.getElementById("campus_region_id").selectedIndex = 0;

     //Reset the region
     for (var i=1; i<region.length; i++) {
        var country_id = region[i].getAttribute("country_id");
        if (country_id.toLowerCase() == country.toLowerCase()) {
            region[i].disabled = false;
        } else {
            region[i].disabled = true;
        }
    }

}

/*
The following javascript is to fix a bug where the map only renders on the right side
of the screen. The javascript changes the position to relative. Which fixes this issue.
 */
function relayout_map() {
    var mapbox = document.getElementById("map");
    var mapbox_canvas = mapbox.getElementsByClassName("mapboxgl-canvas");

    for (var i=0; i < mapbox_canvas.length; i++) {
        mapbox_canvas[i].style.position="relative";
    }
}

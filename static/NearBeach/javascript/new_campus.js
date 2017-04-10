function on_page_load() {
    /* When the page loads, I want it to automatically disable ALL but the first option
     * for the regions. That way no one can do the sneaky and select an OPTION then a
     * country that does not contain that region... sneaky robots
     */
    var campus_region_select = document.getElementById("campus_region_id").getElementsByTagName("option");

    for (var i=1; i<campus_region_select.length; i++) {
        campus_region_select[i].disabled = true;
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
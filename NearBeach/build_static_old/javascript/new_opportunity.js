/**
 * Created by luke on 11/07/17.
 */
function update_customers() {
    /*
    Issue
    ~~~~~
    We do not want the user to pick an organisation and then a customer from a different organisation. This function
    will limit which customer are seen in the "Customer" field to those only belonging to that particular organisation.
    This will work similarly to the Country/Region javascript.

    Method
    ~~~~~~
    1.) Extract out the Organisation ID from the organisation field
    2.) Loop through the customer fields and hide those who are not associated to the organisation
     */
    var organisations_id = document.getElementById('id_organisation_id').value;
    var customer_id = document.getElementById('customer_id');

    // Set customer id to ------
    customer_id.selectedIndex=0;

    /*
    Hide those values we do not want to see anymore
     */
    for (var i=1; i<customer_id.length; i++) {
        var customer_org_id = customer_id[i].getAttribute("organisation_id");
        if (customer_org_id == organisations_id) {
            customer_id[i].disabled=false;
        } else {
            customer_id[i].disabled=true;
        }
    }
}

function probability_update() {
    /*
    Issue
    ~~~~~
    Extract the probability from the dropdown box and update it in the % input

    Method
    ~~~~~~
    1.) Connect the varables to the required fields
    2.) Extract the probability value from the dropdown box
    3.) Apply it to the % input
     */
    var opportuniy_stage = document.getElementById("opportunity_stage");
    var success_probability = document.getElementById("id_opportunity_success_probability");

    success_probability.value = opportuniy_stage[opportuniy_stage.selectedIndex].getAttribute("probability");

}


function apply_organisation_customer(organisation, customer) {
    /*
    After the page loads, we will need to apply the organisation and
    if relivant the customer.
     */
    if (organisation!=null) {
        //Apply the organisation
        var select_field=document.getElementById("id_organisation_id");
        for (i=0;i<select_field.length;i++) {
            if (select_field[i].value==organisation) {
                select_field[i].selected=true;
            }
        }
    }
    if (customer!=null) {
        //Apply the customer
        var select_field=document.getElementById("customer_id");
        for (i=0;i<select_field.length;i++) {
            if (select_field[i].value==customer) {
                select_field[i].selected=true;
            }
        }
    }
}


function grant_access_checkbox(checkbox_id,div_id) {
    /*
    After the user has ticked the checkbox, we will try and find the
    checkbox the user has ticked and determine if we want to hide
    or show the div with the content.
     */
}

function select_groups(select) {
    /*
    Method
    ~~~~~~
    1.) Obtain the text for the current selection
    2.) Look at the <ul id="select_groups_ul">...</ul> and determine if the text is already present
    3.) If text is not present, add on another <li>
     */
    alert("Start");

    var select_value = select.value;
    var dataset = document.getElementById("select_groups_datalist");
    //alert(option);
    alert("Finish");

}

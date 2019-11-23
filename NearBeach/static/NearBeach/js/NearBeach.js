/**
 * Created by luke on 2/07/17.
 */
function update_filter() {
    //Varibales used in the function
    var input,
        filter,
        tr,
        i;

    //Get the value from the search box
    input = document.getElementById("filter_tables");

    //We want to compare apples with apples, make all uppercase
    filter = input.value.toUpperCase();

    //Get all table rows
    tr = document.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        //If the <tr> contains any values of the filter OR has class header, we want to show
        if (tr[i].innerHTML.toUpperCase().indexOf(filter) > -1 || tr[i].className=="header") {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}
function assigned_user_delete(user_id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/assigned_user_delete/' + user_id + '/',
        data: {},
        datatype: 'HTML',
        type: 'POST',
        success: function(data) {
            //Reload assigned users
            load_assigned_user_list();
            load_assigned_user_add();
        },
        error: function() {
            alert("Sorry, but deleting the assigned user did not work");
        }
    })
}
function autoscale_textarea() {
    /*
    This function is designed to autoscale all areas that contain textarea tags.

    Method
    ~~~~~~
    1.) Define the div_sub_content that need scaling in an array
    2.) Loop through array
    3.) Find all textarea contained in that div_content
    4.) Resize to the scroll height + 12px
    5.) End Loop
    6.) If required, hide the div_content
    7.) End Loop

    Notes
    ~~~~~
    Not ALL areas require their textarea to be resized.
     */
    //[div_content_id,hide_after_applying]
    var div_content = [
        ['div_project_history',true],
        ['task_history',true],
        ['div_contact_history',false],
        ['div_organisation_contact',false]
    ];
    for (j=0; j<div_content.length; j++) {
        var div_content_object=document.getElementById(div_content[j][0]); //Has to be plural elements as there could be none
        //If div_content_object does not exist, do not do anything
        if (div_content_object) {
            var all_textareas=div_content_object.getElementsByTagName("textarea");
            for (i=0; i<all_textareas.length; i++) {
                //Default height of 12px
                all_textareas[i].style.height="12px";

                if (all_textareas[i].rows*7<=all_textareas[i].scrollHeight) {
                    all_textareas[i].style.height=all_textareas[i].scrollHeight+12+"px";
                }
            }
            //Only hide the object if true
            if (div_content[j][1]) {
                div_content_object.style = "display: none;";
            }
        }
    }
}


function add_bug(location_id, destination,bug_id, bug_client_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#id_"+bug_id+"_"+bug_client_id).html("Adding...");


    $.ajax({
        url: '/bug_add/' + location_id + '/' + destination + '/' + bug_id + '/' + bug_client_id + '/',
        data: {},
        type: 'POST',
        success: function(data) {
            //$(this).html("Added");
            load_bug_list();
            $("#id_"+bug_id+"_"+bug_client_id).html("Added");
        },
        error: function() {
            alert("We are sorry, we experienced an error trying to add your bug to the " + destination);
        },
    });
}
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

function check_end_date() {
	/* Method
	 * ~~~~~~
	 * 1.) Obtain all element values
	 * 2.) Check to see if the date is actually a date
	 * 3.) (not programmed yet) Edit the day element by removing any days
	 * that are not associated with the choosen month.
	 */
	var year_element = document.getElementById("id_finish_date_year");
	var month_element = document.getElementById("id_finish_date_month");
	var day_element = document.getElementById("id_finish_date_day");
	
	fix_dates(year_element, month_element, day_element);
}


function check_start_date() {
	/* Method
	 * ~~~~~~
	 * 1.) Obtain all element values
	 * 2.) Check to see if the date is actually a date
	 * 3.) (not programmed yet) Edit the day element by removing any days
	 * that are not associated with the choosen month.
	 */
	var year_element = document.getElementById("id_start_date_year");
	var month_element = document.getElementById("id_start_date_month");
	var day_element = document.getElementById("id_start_date_day");

	fix_dates(year_element, month_element, day_element);
}


function fix_dates(year_element, month_element, day_element) {
	/* First we check Feb.
	 * 
	 * Method
	 * ~~~~~~
	 * 1.) Check to see if the year is a leap year using the following;
	 * -- default = 28
	 * -- year / 4.0 = year / 4 = 29
	 * -- year / 100.0 = year / 100 = 28
	 * -- year / 1000.0 = year / 1000 = 29
	 * 2.) If date_element.value > max_days, change value to max_days
	 */
	 if (month_element.value == 2) {
		max_day = 28;
		
		//Hide/Unhide the unrequired dates
		day_element[28].hidden = true; //29th
		day_element[29].hidden = true; //30th
		day_element[30].hidden = true; //31th
		
		// If the year can be divided by 4 cleanly, it is a leap year
		if (parseInt(year_element.value/4) == parseInt(year_element.value)/4.0) {
			max_day = 29;
			day_element[28].hidden = false; //29th
		}
		
		// Exception is on the centruary year, is not a leap year
		if (parseInt(year_element.value/100) == parseInt(year_element.value)/100.0) {
			max_day = 28;
		}
		
		// Unless it falls on a millenium year
		if (parseInt(year_element.value/1000) == parseInt(year_element.value)/1000.0) {
			max_day = 29;
			day_element[28].hidden = false; //29th
		}
		
		// nwo check to see if the day value exceeds the max value
		if (day_element.value > max_day) {
			day_element.value = max_day;
		}


	/* else if the months are;
	 * April - 4th month
	 * June - 6th month
	 * September - 9th month
	 * November - 11th month
	 * Then only 30 days
	 */		
	} else if ((month_element.value == 4) ||
		(month_element.value == 6) ||
		(month_element.value == 9) ||
		(month_element.value == 11)) {
		if (day_element.value > 30) {
				day_element.value = 30;
			}
		
		//Hide/Unhide the unrequired dates
		day_element[28].hidden = false; //29th
		day_element[29].hidden = false; //30th
		day_element[30].hidden = true; //31th
	} else {
		//The rest of the months have 31 days
		//Hide/Unhide the unrequired dates
		day_element[28].hidden = false; //29th
		day_element[29].hidden = false; //30th
		day_element[30].hidden = false; //31th
	}	
} 


function initiate_dates() {
	check_start_date();
	check_end_date();
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// using jQuery to extract the CSRFToken
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
var csrftoken = getCookie('csrftoken');


function ajax_prepare() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
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

function confirm_delete_document(document_key,location_id,destination,folder_id) {
    //bring up modal
    //wait 2 seconds
    //enable button

    $("#confirm_document_delete").modal("show");

    //$(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
    if ((folder_id == null) || (folder_id == 0)) {
        $("#remove_document_confirmed").attr('onclick','delete_document("' + document_key + '","' + location_id + '","' + destination + '")');
    } else {
        $("#remove_document_confirmed").attr('onclick','delete_document("' + document_key + '","' + location_id + '","' + destination + '","' + folder_id + '")');
    }


    setTimeout(function () {
        document.getElementById("remove_document_confirmed").disabled = false;
    }, 2000);
}


function confirm_delete_folder(folder_id,location_id,destination,current_folder_id) {
    //Show the modal - confirm that the user wants to delete the folder
    $("#confirm_folder_delete").modal("show");

    //We need to pass on the information of where to go when the delete button is clicked
    if ((current_folder_id == null) || (current_folder_id == 0)) {
        $("#remove_folder_confirmed").attr('onclick','delete_folder(' + folder_id + ',' + location_id + ',"' + destination + '")');
    } else {
        $("#remove_folder_confirmed").attr('onclick','delete_folder(' + folder_id + ',' + location_id + ',"' + destination + '",' + current_folder_id + ')');
    }

    //We want to make sure the delete button is disabled for 2 seconds
    setTimeout(function () {
        document.getElementById("remove_folder_confirmed").disabled = false;
    }, 2000);
}


function delete_document(document_key,location_id,destination,folder_id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/delete_document/' + document_key + '/',
        data: {},
        dataType: "HTML",
        type: "POST",
        success: function(data) {
            $("#confirm_document_delete").modal("hide"); //Remove the modal
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            alert("Sorry, there was an issue deletng the file");
        }

    })
}


function delete_folder(folder_id,location_id,destination,current_folder_id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/delete_folder/' + folder_id + '/',
        data: {},
        dataType: "HTML",
        type: "POST",
        success: function(data) {
            $("#confirm_folder_delete").modal("hide"); //Remove the modal
            if ((current_folder_id == null) || (current_folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, current_folder_id);
            }
        },
        error: function() {
            alert("Sorry - could not remove folder");
        }

    })
}


function load_document_tree_list(location_id, destination, folder_id) {
    /*
    The URL changes depending on the folder_id. If the folder_id is defined then we want to include it -
    otherwise we do not.
     */
    if (folder_id == null) {
        var url = '/document_tree_list/' + location_id + '/' + destination + '/';
    } else {
        var url = '/document_tree_list/' + location_id + '/' + destination + '/' + folder_id + '/';
    }
    //Load Project History
    $.ajax({
        url: url,
        data: {},
        dataType: 'HTML',
        type: 'GET',
        success: function(data) {
            $('#document_tree_list').html(data);
        },
        error: function() {
            $('#document_tree_list').html('<h2>Document Tree</h2>Sorry, document tree encounted an error and did not load.');
        }
    });
};


function new_folder(location_id,destination,folder_id) {
    console.debug("Sending in new folder information");
//Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Get form data
    var form_data = new FormData($('#new_folder_form')[0]);

    $.ajax({
        url: '/document_tree_folder/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#new_folder_modal").modal("hide"); //Remove the modal
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });
}


function upload_document(location_id,destination,folder_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    //Get form data
    var form_data = new FormData($('#document_upload_form')[0]);

    $.ajax({
        xhr: function() {
            var xhr = new window.XMLHttpRequest();

            // Upload progress
            xhr.upload.addEventListener("progress", function(evt){
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    //Do something with upload progress
                    $("#document_upload_progress").css(
                        'width', percentComplete * 100 + '%'
                    );
                }
           }, false);
           return xhr;
        },

        url: '/document_tree_upload/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            $("#document_upload_progress").css('width','0%;');
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });
}


function upload_url(location_id, destination, folder_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Get form data
    var form_data = new FormData($('#document_url_form')[0]);

    $.ajax({
        url: '/document_tree_url/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#new_url_modal").modal("hide"); //Remove the modal
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });


}


/*
The following code should be inputted into the object you wish to add document list to.

<h2>Document Uploads</h2>
<div class="document_tree_list" id="document_tree_list">
    <h2>Document Tree List</h2>
    Loading...
</div>
 */

function hide_unhide(object_name) {
    var object = document.getElementById(object_name);

    if (object.style.display == "none") {
        object.style.display = "block";
    } else {
        object.style.display = "none";
    }
}
var map;
function initMap(latitude,longitude,title,api_key) {
    var location = {lat: latitude, lng: longitude};
    map = new google.maps.Map(document.getElementById('map'), {
    center:location,
    zoom: 13
    });

    var marker = new google.maps.Marker({
        position: location,
        map: map,
    })
}


/*
The following script will be used to interact with the error modal.
 */

function new_error(error_string) {
    //Show the modal
    $("#error_modal").modal({
        show: true,
        keyboard: true,
        focus: true,
    });

    //Add the error to the current modal
    $("#error_modal_body").append(`<hr>${error_string}`);
}
function initMap(latitude,longitude,title,api_key) {
    mapboxgl.accessToken  = api_key;
    var map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/streets-v9', // stylesheet location
        //center: [latitude,longitude], // starting position [lng, lat]
        center: [longitude,latitude],
        zoom: 15, // starting zoom
    });
    map.on('load', function() {
        map.addLayer({
            "id": "points",
            "type": "symbol",
            "source": {
                "type": "geojson",
                "data": {
                    "type": "FeatureCollection",
                    "features": [{
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            //"coordinates": [latitude,longitude]
                            "coordinates": [longitude,latitude]
                        },
                        "properties": {
                            "title": title,
                            "icon": "marker"
                        }
                    }]
                }
            },
            "layout": {
                "icon-image": "{icon}-15",
                "text-field": "{title}",
                "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
                "text-offset": [0, 0.6],
                "text-anchor": "top"
            }
        })

    });

    map['scrollZoom'].disable();

    $(window).bind('mousewheel DOMMouseScroll', function(event)
    {
        if(event.ctrlKey == true) {
            map['scrollZoom'].enable();
        }
        else {
            map['scrollZoom'].disable();
        }
    });

    //Quickly, relayout the map before anyone knows
    //relayout_map();
    setTimeout(relayout_map, 500);
}


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

void function add_https() {
    /*
    When the user clicks on the organisation's website field, we want to add
    https:// at the start automatically. This is so that the customer does not
    need to enter in this required string. We only need to do this when there
    is nothing in the field
     */

}

void function paste_url() {
    /*
    When the user pastes a URL we want to double check it so that it will pass
    the validation of the form.
     */

}
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

	if ((cost_description.value != '') && (cost_amount.value != '') &&
		((cost_amount.value >= 0) || (cost_amount.value <= 0)) //Work around for if it is a number.
		) {
		add_cost_submit.disabled = false;
	} else {
		add_cost_submit.disabled = true;
	}
}

function render_bug_client_bugs(data, target_id) {
    /*
    Render bug client bugs will render a simple stacked BAR CHART detailing the different stages of bugs on each of
    the different clients.

    Method
    ~~~~~~
    1. Get a unique list of the different bug status
    1. Create a simple array
    2. Create the required graphs :)
     */

    /*
    We will require to get a list of unique bug status. To do this we will first loop through ALL of the different
    bug client results and compile a unique list
     */
    var list_of_bug_status = {};
    for (row in data) {
        //Simplify the code
        var client = data[row],
            bug_status = client["bug_status"];

        //Loop through the bug status'
        for (status in bug_status) {
            //If it exists, it will only make it exist more.
            list_of_bug_status[status] = status;
        }
    }

    //Sort the bug status
    list_of_bug_status = Object.keys(list_of_bug_status).sort(function(a,b){
        return list_of_bug_status[a] - list_of_bug_status[b];
    });

    console.log("Unique bug status: ", list_of_bug_status);

    //Loop through the each bug client, and determine the value of each bug type
    var converted_data = [];
    for (row in data) {
        //Simplify the code
        var client = data[row],
            bug_status = client["bug_status"],
            basic_object = { 'bug_client_name': row };

        //Loop through the unique bug status'
        list_of_bug_status.forEach(function(status) {
            //If the count of the bug client exists, record it.
            //If not - simply put a 0
            if (bug_status[status] == undefined) {
                //We want this field to be a 0 instead of undefinded
                basic_object[status] = 0;
            } else {
                //We want the count of the object.
                basic_object[status] = bug_status[status];
            }
        });

        //Write results to the convered_data
        converted_data.push(basic_object);
    }

    //TEMP VARIABLES//
    var margin = {top: 40, right: 100, bottom: 80, left: 50},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
    //END TEMP VARIABLES//

    console.log("Converted Data: ", converted_data); //The data is now ready :)

    //Setup the x and y range
    var x = d3.scaleBand()
        .rangeRound([0, width], 0.15)
        .paddingInner(0.2)
        .paddingOuter(0.2);

    //Please note y is scale LINEAR!
    var y = d3.scaleLinear()
        .range([height, 0]);

    //Get colour ready
    var color = d3.scaleOrdinal(d3.schemePastel2);

    //Get axis ready
    var xAxis = d3.axisBottom()
        .scale(x);
    var yAxis = d3.axisLeft()
        .scale(y)
        .ticks(10);


    //Prepare the output location
    var output_location = document.getElementById(target_id);
    output_location.innerHTML = "";

    //Create the svg
    var svg = d3.select(output_location).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("data-graph",output_location.id)
        .attr("class", "graph_body")
        .append("g")
        .attr("transform","translate(" + margin.left + "," + margin.top + ")");

    //Assign the colour
    color.domain(
        d3.keys(converted_data[0])
            .filter(function(key) {
                return key !== "bug_client_name";
            })
    );

    //Apply changes to the convert_data - will get it ready for the stacked graph
    converted_data.forEach(function(d) {
        var y0 = 0;
        d.operation = color.domain().map(
            function(name) {
                return {name: name, y0: y0, y1: y0 += +d[name]};
            });
        d.count = d.operation[d.operation.length - 1].y1;
        if (d.count == NaN) { d.count = 0; }
    });

    console.log("Converted data after colours: ", converted_data);

    //Set the x domain
    x.domain(
        converted_data.map(function(d) {
            return d["bug_client_name"];
        })
    );

    //Set the y domain
    y.domain([
        0,
        d3.max(converted_data, function(d) {
            return d.count; })
    ]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Count");

    var stack = svg.selectAll(".location")
        .data(converted_data)
        .enter().append("g")
        .attr("class", "g")
        .attr("transform", function(d) { return "translate(" + x(d["bug_client_name"]) + ",0)"; });

    stack.selectAll("rect")
        .data(function(d) { return d.operation; })
        .enter().append("rect")
        .attr("width", x.bandwidth())
        .attr("y", function(d) { return y(d.y1); })
        .attr("height", function(d) { return y(d.y0) - y(d.y1); })
        .attr("data-value", function(d) { return d.y1-d.y0; }) //The difference between the the values
        .style("fill", function(d) { return color(d.name); });

    var legend = svg.selectAll(".legend")
        .data(color.domain().slice().reverse())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width + 48)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width + 48)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });

    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text("Bug Client Breakdown");


    //X-axis label
    svg.append("text")
        .attr(
            "transform",
            "translate(" + (width/2) + " ," + (height + margin.top + 20) + ")"
        )
        .style("text-anchor", "middle")
        .text("Bug Client Name");

    //Y-axis label
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Count of Bugs");
}
function render_folders(document_folders_results, current_folder) {
	/*
	Render folder function renders each folder. It is a recursive function.
	Each folder it will render it will give an id of the folder number with
	the suffix _folder
	i.e 1_folder

	Step 1
	~~~~~~
	We currently only want the folder for the current location.
	 */
	var folder_results = document_folders_results.filter(function(i, n) {
		return (i.fields.parent_folder_id == current_folder);
	});
	/*
	Step 2
	~~~~~~
	We will loop through each of the folder resules. Make sure that there are
	no sub folder. If there are any sub folder we will call this function
	recursovly with the sub folder information.
	 */
	var content_string = '';
	for (var i=0; i<folder_results.length; i++) {
		content_string += '<li><label>' + folder_results[i].fields.folder_description + '</label>';
		content_string += '<input type="checkbox" id="' + folder_results[i].pk + '_checkbox">';
		content_string += '<ul id="' + folder_results[i].pk + '_folder">';
		content_string += render_folders(document_folders_results, folder_results[i].pk);
		content_string += '</ul></li>';

		/*
		Minor step
		~~~~~~~~~~
		We are now adding the folder to the new_document_location select
		*/
		var new_document_location = document.getElementById("parent_folder_id");
		var folder_location = document.getElementById("folder_location");
		var opt = document.createElement('option');
		opt.value = folder_results[i].pk;
		opt.innerHTML = folder_results[i].fields.folder_description;
		new_document_location.appendChild(opt);
		//folder_location.appendChild(opt);

		//Ok, I am cheating here.
		//Bug with JAVASCRIPT - will now allow me to append the same opt twice.
		var folder_location = document.getElementById("folder_location");
		var opt2 = document.createElement('option');
		opt2.value = folder_results[i].pk;
		opt2.innerHTML = folder_results[i].fields.folder_description;
		folder_location.appendChild(opt2);

	}
	return content_string;

}

function add_new_document() {
	new_document_dialog = document.getElementById("overlay_new_document");
	new_document_dialog.style.visibility = (new_document_dialog.style.visibility == "visible") ? "hidden" : "visible";
}

function add_new_folder() {
    new_folder_dialog = document.getElementById("overlay_new_folder");
    new_folder_dialog.style.visibility = (new_folder_dialog.style.visibility == "visible") ? "hidden" : "visible";
}

function render_documents(document_results, site_url) {
	for (var i=0; i<document_results.length; i++) {
		var content_string = '<a href="';
		if ((document_results[i][3] == '') || (document_results[i][3] == null)) {
            content_string += document_results[i][2];

        } else {
			content_string += site_url + document_results[i][3];
		}
		content_string += '" target="_blank">';
		content_string += document_results[i][1];
		content_string += '</a>';

		if ((document_results[i][4] == null) || (document_results[i][4] == "")) {
			destination_folder = document.getElementById("root_folder");
		} else {
			destination_folder = document.getElementById(document_results[i][4] + "_folder");
		}
		destination_folder.innerHTML = destination_folder.innerHTML + '<br/>' + content_string;

	}
}

function upload_or_link() {
    overlay_upload = document.getElementById("overlay_upload");
    overlay_link = document.getElementById("overlay_link");
    upload_type = document.getElementById("upload_type");


    if (upload_type.selectedIndex == 0) {
        overlay_upload.style.display = "block";
        overlay_link.style.display = "none";
    } else {
        overlay_upload.style.display = "none";
        overlay_link.style.display = "block";
    }

    //Check to make sure if submit needs to be enabled
    enable_submit()
}

function enable_submit() {
	/*
	So I didn't like the spaghetti if statements left here. So I invented this simple
	boolean way to disable and enable the submit button.

	It works by checking to see if there are values in the required fields. It will
	activate the button if either one of the two conditions is met. Simple.
	 */
	id_document = Boolean(document.getElementById("id_document").value != "");
	id_document_url_location = Boolean(document.getElementById("id_document_url_location").value != "");
	id_document_description = Boolean(document.getElementById("id_document_description").value != "");
	id_new_folder = Boolean(document.getElementById("id_folder_description").value == "");

	new_document = document.getElementById("new_document");
	new_folder = document.getElementById("new_folder");
	new_document.disabled = !Boolean((id_document && id_document_description) || (id_document_url_location && id_document_description));
	new_folder.disabled = id_new_folder;
}

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


function load_timesheet(location, destination) {
    $.ajax({
        url: `/timesheet/${ location }/${ destination }/`,
        data: {},
        dataType: 'HTML',
        type: 'GET',
        success: function(data) {
            //Insert the data
            $("#timesheet").html(data);

            //Initiate the data
            timesheet_setup();
        },
        error: function() {
            alert("Sorry, timesheet could not load");
        }
    })
}

function timesheet_setup() {
    /* This function will finish setting up the timesheet - i.e. setup the datetime functions*/
    $( "#id_timesheet_date" ).datetimepicker({
        format: "Y-m-d",
        timepicker:false,
    });


    $("#id_timesheet_start_time").datetimepicker({
        'scrollDefault': 'now',
        datepicker:false,
        format:'H:i',
        allowTimes: [
            '00:00','00:05','00:10','00:15','00:20','00:25','00:30','00:35','00:40','00:45','00:50','00:55',
            '01:00','01:05','01:10','01:15','01:20','01:25','01:30','01:35','01:40','01:45','01:50','01:55',
            '02:00','02:05','02:10','02:15','02:20','02:25','02:30','02:35','02:40','02:45','02:50','02:55',
            '03:00','03:05','03:10','03:15','03:20','03:25','03:30','03:35','03:40','03:45','03:50','03:55',
            '04:00','04:05','04:10','04:15','04:20','04:25','04:30','04:35','04:40','04:45','04:50','04:55',
            '05:00','05:05','05:10','05:15','05:20','05:25','05:30','05:35','05:40','05:45','05:50','05:55',
            '06:00','06:05','06:10','06:15','06:20','06:25','06:30','06:35','06:40','06:45','06:50','06:55',
            '07:00','07:05','07:10','07:15','07:20','07:25','07:30','07:35','07:40','07:45','07:50','07:55',
            '08:00','08:05','08:10','08:15','08:20','08:25','08:30','08:35','08:40','08:45','08:50','08:55',
            '09:00','09:05','09:10','09:15','09:20','09:25','09:30','09:35','09:40','09:45','09:50','09:55',
            '10:00','10:05','10:10','10:15','10:20','10:25','10:30','10:35','10:40','10:45','10:50','10:55',
            '11:00','11:05','11:10','11:15','11:20','11:25','11:30','11:35','11:40','11:45','11:50','11:55',
            '12:00','12:05','12:10','12:15','12:20','12:25','12:30','12:35','12:40','12:45','12:50','12:55',
            '13:00','13:05','13:10','13:15','13:20','13:25','13:30','13:35','13:40','13:45','13:50','13:55',
            '14:00','14:05','14:10','14:15','14:20','14:25','14:30','14:35','14:40','14:45','14:50','14:55',
            '15:00','15:05','15:10','15:15','15:20','15:25','15:30','15:35','15:40','15:45','15:50','15:55',
            '16:00','16:05','16:10','16:15','16:20','16:25','16:30','16:35','16:40','16:45','16:50','16:55',
            '17:00','17:05','17:10','17:15','17:20','17:25','17:30','17:35','17:40','17:45','17:50','17:55',
            '18:00','18:05','18:10','18:15','18:20','18:25','18:30','18:35','18:40','18:45','18:50','18:55',
            '19:00','19:05','19:10','19:15','19:20','19:25','19:30','19:35','19:40','19:45','19:50','19:55',
            '20:00','20:05','20:10','20:15','20:20','20:25','20:30','20:35','20:40','20:45','20:50','20:55',
            '21:00','21:05','21:10','21:15','21:20','21:25','21:30','21:35','21:40','21:45','21:50','21:55',
            '22:00','22:05','22:10','22:15','22:20','22:25','22:30','22:35','22:40','22:45','22:50','22:55',
            '23:00','23:05','23:10','23:15','23:20','23:25','23:30','23:35','23:40','23:45','23:50','23:55'
        ],
        defaultTime: '08:45',
        onSelectTime: function(){
            //Make sure the start time is not greater than the end time
            var start_time = $("#id_timesheet_start_time").val(),
                end_time = $("#id_timesheet_end_time").val();

            if (start_time > end_time) {
                $("#id_timesheet_end_time").val(start_time);
            }
        }
    });

    $("#id_timesheet_end_time").datetimepicker({
        'scrollDefault': 'now',
        datepicker:false,
        format:'H:i',
        allowTimes: [
            '00:00','00:05','00:10','00:15','00:20','00:25','00:30','00:35','00:40','00:45','00:50','00:55',
            '01:00','01:05','01:10','01:15','01:20','01:25','01:30','01:35','01:40','01:45','01:50','01:55',
            '02:00','02:05','02:10','02:15','02:20','02:25','02:30','02:35','02:40','02:45','02:50','02:55',
            '03:00','03:05','03:10','03:15','03:20','03:25','03:30','03:35','03:40','03:45','03:50','03:55',
            '04:00','04:05','04:10','04:15','04:20','04:25','04:30','04:35','04:40','04:45','04:50','04:55',
            '05:00','05:05','05:10','05:15','05:20','05:25','05:30','05:35','05:40','05:45','05:50','05:55',
            '06:00','06:05','06:10','06:15','06:20','06:25','06:30','06:35','06:40','06:45','06:50','06:55',
            '07:00','07:05','07:10','07:15','07:20','07:25','07:30','07:35','07:40','07:45','07:50','07:55',
            '08:00','08:05','08:10','08:15','08:20','08:25','08:30','08:35','08:40','08:45','08:50','08:55',
            '09:00','09:05','09:10','09:15','09:20','09:25','09:30','09:35','09:40','09:45','09:50','09:55',
            '10:00','10:05','10:10','10:15','10:20','10:25','10:30','10:35','10:40','10:45','10:50','10:55',
            '11:00','11:05','11:10','11:15','11:20','11:25','11:30','11:35','11:40','11:45','11:50','11:55',
            '12:00','12:05','12:10','12:15','12:20','12:25','12:30','12:35','12:40','12:45','12:50','12:55',
            '13:00','13:05','13:10','13:15','13:20','13:25','13:30','13:35','13:40','13:45','13:50','13:55',
            '14:00','14:05','14:10','14:15','14:20','14:25','14:30','14:35','14:40','14:45','14:50','14:55',
            '15:00','15:05','15:10','15:15','15:20','15:25','15:30','15:35','15:40','15:45','15:50','15:55',
            '16:00','16:05','16:10','16:15','16:20','16:25','16:30','16:35','16:40','16:45','16:50','16:55',
            '17:00','17:05','17:10','17:15','17:20','17:25','17:30','17:35','17:40','17:45','17:50','17:55',
            '18:00','18:05','18:10','18:15','18:20','18:25','18:30','18:35','18:40','18:45','18:50','18:55',
            '19:00','19:05','19:10','19:15','19:20','19:25','19:30','19:35','19:40','19:45','19:50','19:55',
            '20:00','20:05','20:10','20:15','20:20','20:25','20:30','20:35','20:40','20:45','20:50','20:55',
            '21:00','21:05','21:10','21:15','21:20','21:25','21:30','21:35','21:40','21:45','21:50','21:55',
            '22:00','22:05','22:10','22:15','22:20','22:25','22:30','22:35','22:40','22:45','22:50','22:55',
            '23:00','23:05','23:10','23:15','23:20','23:25','23:30','23:35','23:40','23:45','23:50','23:55'
        ],
        defaultTime: '17:00',
        onSelectTime: function(){
            //Make sure the start time is not greater than the end time
            var start_time = $("#id_timesheet_start_time").val(),
                end_time = $("#id_timesheet_end_time").val();

            if (start_time > end_time) {
                $("#id_timesheet_start_time").val(end_time);
            }
        }
    });

    //Set default dates
    $("#id_timesheet_start_time").val("08:45");
    $("#id_timesheet_end_time").val("17:00");
}
/*
 Copyright (C) Federico Zivolo 2019
 Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
 */var e='undefined'!=typeof window&&'undefined'!=typeof document&&'undefined'!=typeof navigator;const t=function(){const t=['Edge','Trident','Firefox'];for(let o=0;o<t.length;o+=1)if(e&&0<=navigator.userAgent.indexOf(t[o]))return 1;return 0}();function o(e){let t=!1;return()=>{t||(t=!0,window.Promise.resolve().then(()=>{t=!1,e()}))}}function n(e){let o=!1;return()=>{o||(o=!0,setTimeout(()=>{o=!1,e()},t))}}const i=e&&window.Promise;var r=i?o:n;function p(e){return e&&'[object Function]'==={}.toString.call(e)}function d(e,t){if(1!==e.nodeType)return[];const o=e.ownerDocument.defaultView,n=o.getComputedStyle(e,null);return t?n[t]:n}function s(e){return'HTML'===e.nodeName?e:e.parentNode||e.host}function f(e){if(!e)return document.body;switch(e.nodeName){case'HTML':case'BODY':return e.ownerDocument.body;case'#document':return e.body;}const{overflow:t,overflowX:o,overflowY:n}=d(e);return /(auto|scroll|overlay)/.test(t+n+o)?e:f(s(e))}function a(e){return e&&e.referenceNode?e.referenceNode:e}const l=e&&!!(window.MSInputMethodContext&&document.documentMode),m=e&&/MSIE 10/.test(navigator.userAgent);function h(e){return 11===e?l:10===e?m:l||m}function c(e){if(!e)return document.documentElement;const t=h(10)?document.body:null;let o=e.offsetParent||null;for(;o===t&&e.nextElementSibling;)o=(e=e.nextElementSibling).offsetParent;const n=o&&o.nodeName;return n&&'BODY'!==n&&'HTML'!==n?-1!==['TH','TD','TABLE'].indexOf(o.nodeName)&&'static'===d(o,'position')?c(o):o:e?e.ownerDocument.documentElement:document.documentElement}function u(e){const{nodeName:t}=e;return'BODY'!==t&&('HTML'===t||c(e.firstElementChild)===e)}function g(e){return null===e.parentNode?e:g(e.parentNode)}function b(e,t){if(!e||!e.nodeType||!t||!t.nodeType)return document.documentElement;const o=e.compareDocumentPosition(t)&Node.DOCUMENT_POSITION_FOLLOWING,n=o?e:t,i=o?t:e,r=document.createRange();r.setStart(n,0),r.setEnd(i,0);const{commonAncestorContainer:p}=r;if(e!==p&&t!==p||n.contains(i))return u(p)?p:c(p);const d=g(e);return d.host?b(d.host,t):b(e,g(t).host)}function w(e,t='top'){const o='top'===t?'scrollTop':'scrollLeft',n=e.nodeName;if('BODY'===n||'HTML'===n){const t=e.ownerDocument.documentElement,n=e.ownerDocument.scrollingElement||t;return n[o]}return e[o]}function y(e,t,o=!1){const n=w(t,'top'),i=w(t,'left'),r=o?-1:1;return e.top+=n*r,e.bottom+=n*r,e.left+=i*r,e.right+=i*r,e}function E(e,t){const o='x'===t?'Left':'Top',n='Left'==o?'Right':'Bottom';return parseFloat(e[`border${o}Width`],10)+parseFloat(e[`border${n}Width`],10)}function x(e,t,o,n){return Math.max(t[`offset${e}`],t[`scroll${e}`],o[`client${e}`],o[`offset${e}`],o[`scroll${e}`],h(10)?parseInt(o[`offset${e}`])+parseInt(n[`margin${'Height'===e?'Top':'Left'}`])+parseInt(n[`margin${'Height'===e?'Bottom':'Right'}`]):0)}function v(e){const t=e.body,o=e.documentElement,n=h(10)&&getComputedStyle(o);return{height:x('Height',t,o,n),width:x('Width',t,o,n)}}var O=Object.assign||function(e){for(var t,o=1;o<arguments.length;o++)for(var n in t=arguments[o],t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n]);return e};function L(e){return O({},e,{right:e.left+e.width,bottom:e.top+e.height})}function S(e){let t={};try{if(h(10)){t=e.getBoundingClientRect();const o=w(e,'top'),n=w(e,'left');t.top+=o,t.left+=n,t.bottom+=o,t.right+=n}else t=e.getBoundingClientRect()}catch(t){}const o={left:t.left,top:t.top,width:t.right-t.left,height:t.bottom-t.top},n='HTML'===e.nodeName?v(e.ownerDocument):{},i=n.width||e.clientWidth||o.width,r=n.height||e.clientHeight||o.height;let p=e.offsetWidth-i,s=e.offsetHeight-r;if(p||s){const t=d(e);p-=E(t,'x'),s-=E(t,'y'),o.width-=p,o.height-=s}return L(o)}function T(e,t,o=!1){var n=Math.max;const i=h(10),r='HTML'===t.nodeName,p=S(e),s=S(t),a=f(e),l=d(t),m=parseFloat(l.borderTopWidth,10),c=parseFloat(l.borderLeftWidth,10);o&&r&&(s.top=n(s.top,0),s.left=n(s.left,0));let u=L({top:p.top-s.top-m,left:p.left-s.left-c,width:p.width,height:p.height});if(u.marginTop=0,u.marginLeft=0,!i&&r){const e=parseFloat(l.marginTop,10),t=parseFloat(l.marginLeft,10);u.top-=m-e,u.bottom-=m-e,u.left-=c-t,u.right-=c-t,u.marginTop=e,u.marginLeft=t}return(i&&!o?t.contains(a):t===a&&'BODY'!==a.nodeName)&&(u=y(u,t)),u}function D(e,t=!1){var o=Math.max;const n=e.ownerDocument.documentElement,i=T(e,n),r=o(n.clientWidth,window.innerWidth||0),p=o(n.clientHeight,window.innerHeight||0),d=t?0:w(n),s=t?0:w(n,'left'),f={top:d-i.top+i.marginTop,left:s-i.left+i.marginLeft,width:r,height:p};return L(f)}function C(e){const t=e.nodeName;if('BODY'===t||'HTML'===t)return!1;if('fixed'===d(e,'position'))return!0;const o=s(e);return!!o&&C(o)}function N(e){if(!e||!e.parentElement||h())return document.documentElement;let t=e.parentElement;for(;t&&'none'===d(t,'transform');)t=t.parentElement;return t||document.documentElement}function P(e,t,o,n,i=!1){let r={top:0,left:0};const p=i?N(e):b(e,a(t));if('viewport'===n)r=D(p,i);else{let o;'scrollParent'===n?(o=f(s(t)),'BODY'===o.nodeName&&(o=e.ownerDocument.documentElement)):'window'===n?o=e.ownerDocument.documentElement:o=n;const d=T(o,p,i);if('HTML'===o.nodeName&&!C(p)){const{height:t,width:o}=v(e.ownerDocument);r.top+=d.top-d.marginTop,r.bottom=t+d.top,r.left+=d.left-d.marginLeft,r.right=o+d.left}else r=d}o=o||0;const d='number'==typeof o;return r.left+=d?o:o.left||0,r.top+=d?o:o.top||0,r.right-=d?o:o.right||0,r.bottom-=d?o:o.bottom||0,r}function B({width:e,height:t}){return e*t}function H(e,t,o,n,i,r=0){if(-1===e.indexOf('auto'))return e;const p=P(o,n,r,i),d={top:{width:p.width,height:t.top-p.top},right:{width:p.right-t.right,height:p.height},bottom:{width:p.width,height:p.bottom-t.bottom},left:{width:t.left-p.left,height:p.height}},s=Object.keys(d).map((e)=>O({key:e},d[e],{area:B(d[e])})).sort((e,t)=>t.area-e.area),f=s.filter(({width:e,height:t})=>e>=o.clientWidth&&t>=o.clientHeight),a=0<f.length?f[0].key:s[0].key,l=e.split('-')[1];return a+(l?`-${l}`:'')}function W(e,t,o,n=null){const i=n?N(t):b(t,a(o));return T(o,i,n)}function k(e){const t=e.ownerDocument.defaultView,o=t.getComputedStyle(e),n=parseFloat(o.marginTop||0)+parseFloat(o.marginBottom||0),i=parseFloat(o.marginLeft||0)+parseFloat(o.marginRight||0),r={width:e.offsetWidth+i,height:e.offsetHeight+n};return r}function A(e){const t={left:'right',right:'left',bottom:'top',top:'bottom'};return e.replace(/left|right|bottom|top/g,(e)=>t[e])}function M(e,t,o){o=o.split('-')[0];const n=k(e),i={width:n.width,height:n.height},r=-1!==['right','left'].indexOf(o),p=r?'top':'left',d=r?'left':'top',s=r?'height':'width',f=r?'width':'height';return i[p]=t[p]+t[s]/2-n[s]/2,i[d]=o===d?t[d]-n[f]:t[A(d)],i}function F(e,t){return Array.prototype.find?e.find(t):e.filter(t)[0]}function I(e,t,o){if(Array.prototype.findIndex)return e.findIndex((e)=>e[t]===o);const n=F(e,(e)=>e[t]===o);return e.indexOf(n)}function R(e,t,o){const n=void 0===o?e:e.slice(0,I(e,'name',o));return n.forEach((e)=>{e['function']&&console.warn('`modifier.function` is deprecated, use `modifier.fn`!');const o=e['function']||e.fn;e.enabled&&p(o)&&(t.offsets.popper=L(t.offsets.popper),t.offsets.reference=L(t.offsets.reference),t=o(t,e))}),t}function U(){if(this.state.isDestroyed)return;let e={instance:this,styles:{},arrowStyles:{},attributes:{},flipped:!1,offsets:{}};e.offsets.reference=W(this.state,this.popper,this.reference,this.options.positionFixed),e.placement=H(this.options.placement,e.offsets.reference,this.popper,this.reference,this.options.modifiers.flip.boundariesElement,this.options.modifiers.flip.padding),e.originalPlacement=e.placement,e.positionFixed=this.options.positionFixed,e.offsets.popper=M(this.popper,e.offsets.reference,e.placement),e.offsets.popper.position=this.options.positionFixed?'fixed':'absolute',e=R(this.modifiers,e),this.state.isCreated?this.options.onUpdate(e):(this.state.isCreated=!0,this.options.onCreate(e))}function Y(e,t){return e.some(({name:e,enabled:o})=>o&&e===t)}function V(e){const t=[!1,'ms','Webkit','Moz','O'],o=e.charAt(0).toUpperCase()+e.slice(1);for(let n=0;n<t.length;n++){const i=t[n],r=i?`${i}${o}`:e;if('undefined'!=typeof document.body.style[r])return r}return null}function j(){return this.state.isDestroyed=!0,Y(this.modifiers,'applyStyle')&&(this.popper.removeAttribute('x-placement'),this.popper.style.position='',this.popper.style.top='',this.popper.style.left='',this.popper.style.right='',this.popper.style.bottom='',this.popper.style.willChange='',this.popper.style[V('transform')]=''),this.disableEventListeners(),this.options.removeOnDestroy&&this.popper.parentNode.removeChild(this.popper),this}function K(e){const t=e.ownerDocument;return t?t.defaultView:window}function q(e,t,o,n){const i='BODY'===e.nodeName,r=i?e.ownerDocument.defaultView:e;r.addEventListener(t,o,{passive:!0}),i||q(f(r.parentNode),t,o,n),n.push(r)}function z(e,t,o,n){o.updateBound=n,K(e).addEventListener('resize',o.updateBound,{passive:!0});const i=f(e);return q(i,'scroll',o.updateBound,o.scrollParents),o.scrollElement=i,o.eventsEnabled=!0,o}function G(){this.state.eventsEnabled||(this.state=z(this.reference,this.options,this.state,this.scheduleUpdate))}function _(e,t){return K(e).removeEventListener('resize',t.updateBound),t.scrollParents.forEach((e)=>{e.removeEventListener('scroll',t.updateBound)}),t.updateBound=null,t.scrollParents=[],t.scrollElement=null,t.eventsEnabled=!1,t}function X(){this.state.eventsEnabled&&(cancelAnimationFrame(this.scheduleUpdate),this.state=_(this.reference,this.state))}function J(e){return''!==e&&!isNaN(parseFloat(e))&&isFinite(e)}function Q(e,t){Object.keys(t).forEach((o)=>{let n='';-1!==['width','height','top','right','bottom','left'].indexOf(o)&&J(t[o])&&(n='px'),e.style[o]=t[o]+n})}function Z(e,t){Object.keys(t).forEach(function(o){const n=t[o];!1===n?e.removeAttribute(o):e.setAttribute(o,t[o])})}function $(e){return Q(e.instance.popper,e.styles),Z(e.instance.popper,e.attributes),e.arrowElement&&Object.keys(e.arrowStyles).length&&Q(e.arrowElement,e.arrowStyles),e}function ee(e,t,o,n,i){const r=W(i,t,e,o.positionFixed),p=H(o.placement,r,t,e,o.modifiers.flip.boundariesElement,o.modifiers.flip.padding);return t.setAttribute('x-placement',p),Q(t,{position:o.positionFixed?'fixed':'absolute'}),o}function te(e,t){const{popper:o,reference:n}=e.offsets,{round:i,floor:r}=Math,p=(e)=>e,d=i(n.width),s=i(o.width),f=-1!==['left','right'].indexOf(e.placement),a=-1!==e.placement.indexOf('-'),l=t?f||a||d%2==s%2?i:r:p,m=t?i:p;return{left:l(1==d%2&&1==s%2&&!a&&t?o.left-1:o.left),top:m(o.top),bottom:m(o.bottom),right:l(o.right)}}const oe=e&&/Firefox/i.test(navigator.userAgent);function ne(e,t){const{x:o,y:n}=t,{popper:i}=e.offsets,r=F(e.instance.modifiers,(e)=>'applyStyle'===e.name).gpuAcceleration;void 0!==r&&console.warn('WARNING: `gpuAcceleration` option moved to `computeStyle` modifier and will not be supported in future versions of Popper.js!');const p=void 0===r?t.gpuAcceleration:r,d=c(e.instance.popper),s=S(d),f={position:i.position},a=te(e,2>window.devicePixelRatio||!oe),l='bottom'===o?'top':'bottom',m='right'===n?'left':'right',h=V('transform');let u,g;if(g='bottom'==l?'HTML'===d.nodeName?-d.clientHeight+a.bottom:-s.height+a.bottom:a.top,u='right'==m?'HTML'===d.nodeName?-d.clientWidth+a.right:-s.width+a.right:a.left,p&&h)f[h]=`translate3d(${u}px, ${g}px, 0)`,f[l]=0,f[m]=0,f.willChange='transform';else{const e='bottom'==l?-1:1,t='right'==m?-1:1;f[l]=g*e,f[m]=u*t,f.willChange=`${l}, ${m}`}const b={"x-placement":e.placement};return e.attributes=O({},b,e.attributes),e.styles=O({},f,e.styles),e.arrowStyles=O({},e.offsets.arrow,e.arrowStyles),e}function ie(e,t,o){const n=F(e,({name:e})=>e===t),i=!!n&&e.some((e)=>e.name===o&&e.enabled&&e.order<n.order);if(!i){const e=`\`${t}\``,n=`\`${o}\``;console.warn(`${n} modifier is required by ${e} modifier in order to work, be sure to include it before ${e}!`)}return i}function re(e,t){if(!ie(e.instance.modifiers,'arrow','keepTogether'))return e;let o=t.element;if('string'==typeof o){if(o=e.instance.popper.querySelector(o),!o)return e;}else if(!e.instance.popper.contains(o))return console.warn('WARNING: `arrow.element` must be child of its popper element!'),e;const n=e.placement.split('-')[0],{popper:i,reference:r}=e.offsets,p=-1!==['left','right'].indexOf(n),s=p?'height':'width',f=p?'Top':'Left',a=f.toLowerCase(),l=p?'left':'top',m=p?'bottom':'right',h=k(o)[s];r[m]-h<i[a]&&(e.offsets.popper[a]-=i[a]-(r[m]-h)),r[a]+h>i[m]&&(e.offsets.popper[a]+=r[a]+h-i[m]),e.offsets.popper=L(e.offsets.popper);const c=r[a]+r[s]/2-h/2,u=d(e.instance.popper),g=parseFloat(u[`margin${f}`],10),b=parseFloat(u[`border${f}Width`],10);let w=c-e.offsets.popper[a]-g-b;return w=Math.max(Math.min(i[s]-h,w),0),e.arrowElement=o,e.offsets.arrow={[a]:Math.round(w),[l]:''},e}function pe(e){if('end'===e)return'start';return'start'===e?'end':e}var de=['auto-start','auto','auto-end','top-start','top','top-end','right-start','right','right-end','bottom-end','bottom','bottom-start','left-end','left','left-start'];const se=de.slice(3);function fe(e,t=!1){const o=se.indexOf(e),n=se.slice(o+1).concat(se.slice(0,o));return t?n.reverse():n}const ae={FLIP:'flip',CLOCKWISE:'clockwise',COUNTERCLOCKWISE:'counterclockwise'};function le(e,t){if(Y(e.instance.modifiers,'inner'))return e;if(e.flipped&&e.placement===e.originalPlacement)return e;const o=P(e.instance.popper,e.instance.reference,t.padding,t.boundariesElement,e.positionFixed);let n=e.placement.split('-')[0],i=A(n),r=e.placement.split('-')[1]||'',p=[];switch(t.behavior){case ae.FLIP:p=[n,i];break;case ae.CLOCKWISE:p=fe(n);break;case ae.COUNTERCLOCKWISE:p=fe(n,!0);break;default:p=t.behavior;}return p.forEach((d,s)=>{if(n!==d||p.length===s+1)return e;n=e.placement.split('-')[0],i=A(n);const f=e.offsets.popper,a=e.offsets.reference,l=Math.floor,m='left'===n&&l(f.right)>l(a.left)||'right'===n&&l(f.left)<l(a.right)||'top'===n&&l(f.bottom)>l(a.top)||'bottom'===n&&l(f.top)<l(a.bottom),h=l(f.left)<l(o.left),c=l(f.right)>l(o.right),u=l(f.top)<l(o.top),g=l(f.bottom)>l(o.bottom),b='left'===n&&h||'right'===n&&c||'top'===n&&u||'bottom'===n&&g,w=-1!==['top','bottom'].indexOf(n),y=!!t.flipVariations&&(w&&'start'===r&&h||w&&'end'===r&&c||!w&&'start'===r&&u||!w&&'end'===r&&g),E=!!t.flipVariationsByContent&&(w&&'start'===r&&c||w&&'end'===r&&h||!w&&'start'===r&&g||!w&&'end'===r&&u),x=y||E;(m||b||x)&&(e.flipped=!0,(m||b)&&(n=p[s+1]),x&&(r=pe(r)),e.placement=n+(r?'-'+r:''),e.offsets.popper=O({},e.offsets.popper,M(e.instance.popper,e.offsets.reference,e.placement)),e=R(e.instance.modifiers,e,'flip'))}),e}function me(e){const{popper:t,reference:o}=e.offsets,n=e.placement.split('-')[0],i=Math.floor,r=-1!==['top','bottom'].indexOf(n),p=r?'right':'bottom',d=r?'left':'top',s=r?'width':'height';return t[p]<i(o[d])&&(e.offsets.popper[d]=i(o[d])-t[s]),t[d]>i(o[p])&&(e.offsets.popper[d]=i(o[p])),e}function he(e,t,o,n){var i=Math.max;const r=e.match(/((?:\-|\+)?\d*\.?\d*)(.*)/),p=+r[1],d=r[2];if(!p)return e;if(0===d.indexOf('%')){let e;switch(d){case'%p':e=o;break;case'%':case'%r':default:e=n;}const i=L(e);return i[t]/100*p}if('vh'===d||'vw'===d){let e;return e='vh'===d?i(document.documentElement.clientHeight,window.innerHeight||0):i(document.documentElement.clientWidth,window.innerWidth||0),e/100*p}return p}function ce(e,t,o,n){const i=[0,0],r=-1!==['right','left'].indexOf(n),p=e.split(/(\+|\-)/).map((e)=>e.trim()),d=p.indexOf(F(p,(e)=>-1!==e.search(/,|\s/)));p[d]&&-1===p[d].indexOf(',')&&console.warn('Offsets separated by white space(s) are deprecated, use a comma (,) instead.');const s=/\s*,\s*|\s+/;let f=-1===d?[p]:[p.slice(0,d).concat([p[d].split(s)[0]]),[p[d].split(s)[1]].concat(p.slice(d+1))];return f=f.map((e,n)=>{const i=(1===n?!r:r)?'height':'width';let p=!1;return e.reduce((e,t)=>''===e[e.length-1]&&-1!==['+','-'].indexOf(t)?(e[e.length-1]=t,p=!0,e):p?(e[e.length-1]+=t,p=!1,e):e.concat(t),[]).map((e)=>he(e,i,t,o))}),f.forEach((e,t)=>{e.forEach((o,n)=>{J(o)&&(i[t]+=o*('-'===e[n-1]?-1:1))})}),i}function ue(e,{offset:t}){const{placement:o,offsets:{popper:n,reference:i}}=e,r=o.split('-')[0];let p;return p=J(+t)?[+t,0]:ce(t,n,i,r),'left'===r?(n.top+=p[0],n.left-=p[1]):'right'===r?(n.top+=p[0],n.left+=p[1]):'top'===r?(n.left+=p[0],n.top-=p[1]):'bottom'===r&&(n.left+=p[0],n.top+=p[1]),e.popper=n,e}function ge(e,t){let o=t.boundariesElement||c(e.instance.popper);e.instance.reference===o&&(o=c(o));const n=V('transform'),i=e.instance.popper.style,{top:r,left:p,[n]:d}=i;i.top='',i.left='',i[n]='';const s=P(e.instance.popper,e.instance.reference,t.padding,o,e.positionFixed);i.top=r,i.left=p,i[n]=d,t.boundaries=s;const f=t.priority;let a=e.offsets.popper;const l={primary(e){let o=a[e];return a[e]<s[e]&&!t.escapeWithReference&&(o=Math.max(a[e],s[e])),{[e]:o}},secondary(e){const o='right'===e?'left':'top';let n=a[o];return a[e]>s[e]&&!t.escapeWithReference&&(n=Math.min(a[o],s[e]-('right'===e?a.width:a.height))),{[o]:n}}};return f.forEach((e)=>{const t=-1===['left','top'].indexOf(e)?'secondary':'primary';a=O({},a,l[t](e))}),e.offsets.popper=a,e}function be(e){const t=e.placement,o=t.split('-')[0],n=t.split('-')[1];if(n){const{reference:t,popper:i}=e.offsets,r=-1!==['bottom','top'].indexOf(o),p=r?'left':'top',d=r?'width':'height',s={start:{[p]:t[p]},end:{[p]:t[p]+t[d]-i[d]}};e.offsets.popper=O({},i,s[n])}return e}function we(e){if(!ie(e.instance.modifiers,'hide','preventOverflow'))return e;const t=e.offsets.reference,o=F(e.instance.modifiers,(e)=>'preventOverflow'===e.name).boundaries;if(t.bottom<o.top||t.left>o.right||t.top>o.bottom||t.right<o.left){if(!0===e.hide)return e;e.hide=!0,e.attributes['x-out-of-boundaries']=''}else{if(!1===e.hide)return e;e.hide=!1,e.attributes['x-out-of-boundaries']=!1}return e}function ye(e){const t=e.placement,o=t.split('-')[0],{popper:n,reference:i}=e.offsets,r=-1!==['left','right'].indexOf(o),p=-1===['top','left'].indexOf(o);return n[r?'left':'top']=i[o]-(p?n[r?'width':'height']:0),e.placement=A(t),e.offsets.popper=L(n),e}var Ee={shift:{order:100,enabled:!0,fn:be},offset:{order:200,enabled:!0,fn:ue,offset:0},preventOverflow:{order:300,enabled:!0,fn:ge,priority:['left','right','top','bottom'],padding:5,boundariesElement:'scrollParent'},keepTogether:{order:400,enabled:!0,fn:me},arrow:{order:500,enabled:!0,fn:re,element:'[x-arrow]'},flip:{order:600,enabled:!0,fn:le,behavior:'flip',padding:5,boundariesElement:'viewport',flipVariations:!1,flipVariationsByContent:!1},inner:{order:700,enabled:!1,fn:ye},hide:{order:800,enabled:!0,fn:we},computeStyle:{order:850,enabled:!0,fn:ne,gpuAcceleration:!0,x:'bottom',y:'right'},applyStyle:{order:900,enabled:!0,fn:$,onLoad:ee,gpuAcceleration:void 0}},xe={placement:'bottom',positionFixed:!1,eventsEnabled:!0,removeOnDestroy:!1,onCreate:()=>{},onUpdate:()=>{},modifiers:Ee};class ve{constructor(e,t,o={}){this.scheduleUpdate=()=>requestAnimationFrame(this.update),this.update=r(this.update.bind(this)),this.options=O({},ve.Defaults,o),this.state={isDestroyed:!1,isCreated:!1,scrollParents:[]},this.reference=e&&e.jquery?e[0]:e,this.popper=t&&t.jquery?t[0]:t,this.options.modifiers={},Object.keys(O({},ve.Defaults.modifiers,o.modifiers)).forEach((e)=>{this.options.modifiers[e]=O({},ve.Defaults.modifiers[e]||{},o.modifiers?o.modifiers[e]:{})}),this.modifiers=Object.keys(this.options.modifiers).map((e)=>O({name:e},this.options.modifiers[e])).sort((e,t)=>e.order-t.order),this.modifiers.forEach((e)=>{e.enabled&&p(e.onLoad)&&e.onLoad(this.reference,this.popper,this.options,e,this.state)}),this.update();const n=this.options.eventsEnabled;n&&this.enableEventListeners(),this.state.eventsEnabled=n}update(){return U.call(this)}destroy(){return j.call(this)}enableEventListeners(){return G.call(this)}disableEventListeners(){return X.call(this)}}ve.Utils=('undefined'==typeof window?global:window).PopperUtils,ve.placements=de,ve.Defaults=xe;export default ve;
//# sourceMappingURL=popper.min.js.map

/*!
  * Bootstrap v4.3.1 (https://getbootstrap.com/)
  * Copyright 2011-2019 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
  */
!function(t,e){"object"==typeof exports&&"undefined"!=typeof module?e(exports,require("jquery"),require("popper.js")):"function"==typeof define&&define.amd?define(["exports","jquery","popper.js"],e):e((t=t||self).bootstrap={},t.jQuery,t.Popper)}(this,function(t,g,u){"use strict";function i(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}function s(t,e,n){return e&&i(t.prototype,e),n&&i(t,n),t}function l(o){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{},e=Object.keys(r);"function"==typeof Object.getOwnPropertySymbols&&(e=e.concat(Object.getOwnPropertySymbols(r).filter(function(t){return Object.getOwnPropertyDescriptor(r,t).enumerable}))),e.forEach(function(t){var e,n,i;e=o,i=r[n=t],n in e?Object.defineProperty(e,n,{value:i,enumerable:!0,configurable:!0,writable:!0}):e[n]=i})}return o}g=g&&g.hasOwnProperty("default")?g.default:g,u=u&&u.hasOwnProperty("default")?u.default:u;var e="transitionend";function n(t){var e=this,n=!1;return g(this).one(_.TRANSITION_END,function(){n=!0}),setTimeout(function(){n||_.triggerTransitionEnd(e)},t),this}var _={TRANSITION_END:"bsTransitionEnd",getUID:function(t){for(;t+=~~(1e6*Math.random()),document.getElementById(t););return t},getSelectorFromElement:function(t){var e=t.getAttribute("data-target");if(!e||"#"===e){var n=t.getAttribute("href");e=n&&"#"!==n?n.trim():""}try{return document.querySelector(e)?e:null}catch(t){return null}},getTransitionDurationFromElement:function(t){if(!t)return 0;var e=g(t).css("transition-duration"),n=g(t).css("transition-delay"),i=parseFloat(e),o=parseFloat(n);return i||o?(e=e.split(",")[0],n=n.split(",")[0],1e3*(parseFloat(e)+parseFloat(n))):0},reflow:function(t){return t.offsetHeight},triggerTransitionEnd:function(t){g(t).trigger(e)},supportsTransitionEnd:function(){return Boolean(e)},isElement:function(t){return(t[0]||t).nodeType},typeCheckConfig:function(t,e,n){for(var i in n)if(Object.prototype.hasOwnProperty.call(n,i)){var o=n[i],r=e[i],s=r&&_.isElement(r)?"element":(a=r,{}.toString.call(a).match(/\s([a-z]+)/i)[1].toLowerCase());if(!new RegExp(o).test(s))throw new Error(t.toUpperCase()+': Option "'+i+'" provided type "'+s+'" but expected type "'+o+'".')}var a},findShadowRoot:function(t){if(!document.documentElement.attachShadow)return null;if("function"!=typeof t.getRootNode)return t instanceof ShadowRoot?t:t.parentNode?_.findShadowRoot(t.parentNode):null;var e=t.getRootNode();return e instanceof ShadowRoot?e:null}};g.fn.emulateTransitionEnd=n,g.event.special[_.TRANSITION_END]={bindType:e,delegateType:e,handle:function(t){if(g(t.target).is(this))return t.handleObj.handler.apply(this,arguments)}};var o="alert",r="bs.alert",a="."+r,c=g.fn[o],h={CLOSE:"close"+a,CLOSED:"closed"+a,CLICK_DATA_API:"click"+a+".data-api"},f="alert",d="fade",m="show",p=function(){function i(t){this._element=t}var t=i.prototype;return t.close=function(t){var e=this._element;t&&(e=this._getRootElement(t)),this._triggerCloseEvent(e).isDefaultPrevented()||this._removeElement(e)},t.dispose=function(){g.removeData(this._element,r),this._element=null},t._getRootElement=function(t){var e=_.getSelectorFromElement(t),n=!1;return e&&(n=document.querySelector(e)),n||(n=g(t).closest("."+f)[0]),n},t._triggerCloseEvent=function(t){var e=g.Event(h.CLOSE);return g(t).trigger(e),e},t._removeElement=function(e){var n=this;if(g(e).removeClass(m),g(e).hasClass(d)){var t=_.getTransitionDurationFromElement(e);g(e).one(_.TRANSITION_END,function(t){return n._destroyElement(e,t)}).emulateTransitionEnd(t)}else this._destroyElement(e)},t._destroyElement=function(t){g(t).detach().trigger(h.CLOSED).remove()},i._jQueryInterface=function(n){return this.each(function(){var t=g(this),e=t.data(r);e||(e=new i(this),t.data(r,e)),"close"===n&&e[n](this)})},i._handleDismiss=function(e){return function(t){t&&t.preventDefault(),e.close(this)}},s(i,null,[{key:"VERSION",get:function(){return"4.3.1"}}]),i}();g(document).on(h.CLICK_DATA_API,'[data-dismiss="alert"]',p._handleDismiss(new p)),g.fn[o]=p._jQueryInterface,g.fn[o].Constructor=p,g.fn[o].noConflict=function(){return g.fn[o]=c,p._jQueryInterface};var v="button",y="bs.button",E="."+y,C=".data-api",T=g.fn[v],S="active",b="btn",I="focus",D='[data-toggle^="button"]',w='[data-toggle="buttons"]',A='input:not([type="hidden"])',N=".active",O=".btn",k={CLICK_DATA_API:"click"+E+C,FOCUS_BLUR_DATA_API:"focus"+E+C+" blur"+E+C},P=function(){function n(t){this._element=t}var t=n.prototype;return t.toggle=function(){var t=!0,e=!0,n=g(this._element).closest(w)[0];if(n){var i=this._element.querySelector(A);if(i){if("radio"===i.type)if(i.checked&&this._element.classList.contains(S))t=!1;else{var o=n.querySelector(N);o&&g(o).removeClass(S)}if(t){if(i.hasAttribute("disabled")||n.hasAttribute("disabled")||i.classList.contains("disabled")||n.classList.contains("disabled"))return;i.checked=!this._element.classList.contains(S),g(i).trigger("change")}i.focus(),e=!1}}e&&this._element.setAttribute("aria-pressed",!this._element.classList.contains(S)),t&&g(this._element).toggleClass(S)},t.dispose=function(){g.removeData(this._element,y),this._element=null},n._jQueryInterface=function(e){return this.each(function(){var t=g(this).data(y);t||(t=new n(this),g(this).data(y,t)),"toggle"===e&&t[e]()})},s(n,null,[{key:"VERSION",get:function(){return"4.3.1"}}]),n}();g(document).on(k.CLICK_DATA_API,D,function(t){t.preventDefault();var e=t.target;g(e).hasClass(b)||(e=g(e).closest(O)),P._jQueryInterface.call(g(e),"toggle")}).on(k.FOCUS_BLUR_DATA_API,D,function(t){var e=g(t.target).closest(O)[0];g(e).toggleClass(I,/^focus(in)?$/.test(t.type))}),g.fn[v]=P._jQueryInterface,g.fn[v].Constructor=P,g.fn[v].noConflict=function(){return g.fn[v]=T,P._jQueryInterface};var L="carousel",j="bs.carousel",H="."+j,R=".data-api",x=g.fn[L],F={interval:5e3,keyboard:!0,slide:!1,pause:"hover",wrap:!0,touch:!0},U={interval:"(number|boolean)",keyboard:"boolean",slide:"(boolean|string)",pause:"(string|boolean)",wrap:"boolean",touch:"boolean"},W="next",q="prev",M="left",K="right",Q={SLIDE:"slide"+H,SLID:"slid"+H,KEYDOWN:"keydown"+H,MOUSEENTER:"mouseenter"+H,MOUSELEAVE:"mouseleave"+H,TOUCHSTART:"touchstart"+H,TOUCHMOVE:"touchmove"+H,TOUCHEND:"touchend"+H,POINTERDOWN:"pointerdown"+H,POINTERUP:"pointerup"+H,DRAG_START:"dragstart"+H,LOAD_DATA_API:"load"+H+R,CLICK_DATA_API:"click"+H+R},B="carousel",V="active",Y="slide",z="carousel-item-right",X="carousel-item-left",$="carousel-item-next",G="carousel-item-prev",J="pointer-event",Z=".active",tt=".active.carousel-item",et=".carousel-item",nt=".carousel-item img",it=".carousel-item-next, .carousel-item-prev",ot=".carousel-indicators",rt="[data-slide], [data-slide-to]",st='[data-ride="carousel"]',at={TOUCH:"touch",PEN:"pen"},lt=function(){function r(t,e){this._items=null,this._interval=null,this._activeElement=null,this._isPaused=!1,this._isSliding=!1,this.touchTimeout=null,this.touchStartX=0,this.touchDeltaX=0,this._config=this._getConfig(e),this._element=t,this._indicatorsElement=this._element.querySelector(ot),this._touchSupported="ontouchstart"in document.documentElement||0<navigator.maxTouchPoints,this._pointerEvent=Boolean(window.PointerEvent||window.MSPointerEvent),this._addEventListeners()}var t=r.prototype;return t.next=function(){this._isSliding||this._slide(W)},t.nextWhenVisible=function(){!document.hidden&&g(this._element).is(":visible")&&"hidden"!==g(this._element).css("visibility")&&this.next()},t.prev=function(){this._isSliding||this._slide(q)},t.pause=function(t){t||(this._isPaused=!0),this._element.querySelector(it)&&(_.triggerTransitionEnd(this._element),this.cycle(!0)),clearInterval(this._interval),this._interval=null},t.cycle=function(t){t||(this._isPaused=!1),this._interval&&(clearInterval(this._interval),this._interval=null),this._config.interval&&!this._isPaused&&(this._interval=setInterval((document.visibilityState?this.nextWhenVisible:this.next).bind(this),this._config.interval))},t.to=function(t){var e=this;this._activeElement=this._element.querySelector(tt);var n=this._getItemIndex(this._activeElement);if(!(t>this._items.length-1||t<0))if(this._isSliding)g(this._element).one(Q.SLID,function(){return e.to(t)});else{if(n===t)return this.pause(),void this.cycle();var i=n<t?W:q;this._slide(i,this._items[t])}},t.dispose=function(){g(this._element).off(H),g.removeData(this._element,j),this._items=null,this._config=null,this._element=null,this._interval=null,this._isPaused=null,this._isSliding=null,this._activeElement=null,this._indicatorsElement=null},t._getConfig=function(t){return t=l({},F,t),_.typeCheckConfig(L,t,U),t},t._handleSwipe=function(){var t=Math.abs(this.touchDeltaX);if(!(t<=40)){var e=t/this.touchDeltaX;0<e&&this.prev(),e<0&&this.next()}},t._addEventListeners=function(){var e=this;this._config.keyboard&&g(this._element).on(Q.KEYDOWN,function(t){return e._keydown(t)}),"hover"===this._config.pause&&g(this._element).on(Q.MOUSEENTER,function(t){return e.pause(t)}).on(Q.MOUSELEAVE,function(t){return e.cycle(t)}),this._config.touch&&this._addTouchEventListeners()},t._addTouchEventListeners=function(){var n=this;if(this._touchSupported){var e=function(t){n._pointerEvent&&at[t.originalEvent.pointerType.toUpperCase()]?n.touchStartX=t.originalEvent.clientX:n._pointerEvent||(n.touchStartX=t.originalEvent.touches[0].clientX)},i=function(t){n._pointerEvent&&at[t.originalEvent.pointerType.toUpperCase()]&&(n.touchDeltaX=t.originalEvent.clientX-n.touchStartX),n._handleSwipe(),"hover"===n._config.pause&&(n.pause(),n.touchTimeout&&clearTimeout(n.touchTimeout),n.touchTimeout=setTimeout(function(t){return n.cycle(t)},500+n._config.interval))};g(this._element.querySelectorAll(nt)).on(Q.DRAG_START,function(t){return t.preventDefault()}),this._pointerEvent?(g(this._element).on(Q.POINTERDOWN,function(t){return e(t)}),g(this._element).on(Q.POINTERUP,function(t){return i(t)}),this._element.classList.add(J)):(g(this._element).on(Q.TOUCHSTART,function(t){return e(t)}),g(this._element).on(Q.TOUCHMOVE,function(t){var e;(e=t).originalEvent.touches&&1<e.originalEvent.touches.length?n.touchDeltaX=0:n.touchDeltaX=e.originalEvent.touches[0].clientX-n.touchStartX}),g(this._element).on(Q.TOUCHEND,function(t){return i(t)}))}},t._keydown=function(t){if(!/input|textarea/i.test(t.target.tagName))switch(t.which){case 37:t.preventDefault(),this.prev();break;case 39:t.preventDefault(),this.next()}},t._getItemIndex=function(t){return this._items=t&&t.parentNode?[].slice.call(t.parentNode.querySelectorAll(et)):[],this._items.indexOf(t)},t._getItemByDirection=function(t,e){var n=t===W,i=t===q,o=this._getItemIndex(e),r=this._items.length-1;if((i&&0===o||n&&o===r)&&!this._config.wrap)return e;var s=(o+(t===q?-1:1))%this._items.length;return-1===s?this._items[this._items.length-1]:this._items[s]},t._triggerSlideEvent=function(t,e){var n=this._getItemIndex(t),i=this._getItemIndex(this._element.querySelector(tt)),o=g.Event(Q.SLIDE,{relatedTarget:t,direction:e,from:i,to:n});return g(this._element).trigger(o),o},t._setActiveIndicatorElement=function(t){if(this._indicatorsElement){var e=[].slice.call(this._indicatorsElement.querySelectorAll(Z));g(e).removeClass(V);var n=this._indicatorsElement.children[this._getItemIndex(t)];n&&g(n).addClass(V)}},t._slide=function(t,e){var n,i,o,r=this,s=this._element.querySelector(tt),a=this._getItemIndex(s),l=e||s&&this._getItemByDirection(t,s),c=this._getItemIndex(l),h=Boolean(this._interval);if(o=t===W?(n=X,i=$,M):(n=z,i=G,K),l&&g(l).hasClass(V))this._isSliding=!1;else if(!this._triggerSlideEvent(l,o).isDefaultPrevented()&&s&&l){this._isSliding=!0,h&&this.pause(),this._setActiveIndicatorElement(l);var u=g.Event(Q.SLID,{relatedTarget:l,direction:o,from:a,to:c});if(g(this._element).hasClass(Y)){g(l).addClass(i),_.reflow(l),g(s).addClass(n),g(l).addClass(n);var f=parseInt(l.getAttribute("data-interval"),10);this._config.interval=f?(this._config.defaultInterval=this._config.defaultInterval||this._config.interval,f):this._config.defaultInterval||this._config.interval;var d=_.getTransitionDurationFromElement(s);g(s).one(_.TRANSITION_END,function(){g(l).removeClass(n+" "+i).addClass(V),g(s).removeClass(V+" "+i+" "+n),r._isSliding=!1,setTimeout(function(){return g(r._element).trigger(u)},0)}).emulateTransitionEnd(d)}else g(s).removeClass(V),g(l).addClass(V),this._isSliding=!1,g(this._element).trigger(u);h&&this.cycle()}},r._jQueryInterface=function(i){return this.each(function(){var t=g(this).data(j),e=l({},F,g(this).data());"object"==typeof i&&(e=l({},e,i));var n="string"==typeof i?i:e.slide;if(t||(t=new r(this,e),g(this).data(j,t)),"number"==typeof i)t.to(i);else if("string"==typeof n){if("undefined"==typeof t[n])throw new TypeError('No method named "'+n+'"');t[n]()}else e.interval&&e.ride&&(t.pause(),t.cycle())})},r._dataApiClickHandler=function(t){var e=_.getSelectorFromElement(this);if(e){var n=g(e)[0];if(n&&g(n).hasClass(B)){var i=l({},g(n).data(),g(this).data()),o=this.getAttribute("data-slide-to");o&&(i.interval=!1),r._jQueryInterface.call(g(n),i),o&&g(n).data(j).to(o),t.preventDefault()}}},s(r,null,[{key:"VERSION",get:function(){return"4.3.1"}},{key:"Default",get:function(){return F}}]),r}();g(document).on(Q.CLICK_DATA_API,rt,lt._dataApiClickHandler),g(window).on(Q.LOAD_DATA_API,function(){for(var t=[].slice.call(document.querySelectorAll(st)),e=0,n=t.length;e<n;e++){var i=g(t[e]);lt._jQueryInterface.call(i,i.data())}}),g.fn[L]=lt._jQueryInterface,g.fn[L].Constructor=lt,g.fn[L].noConflict=function(){return g.fn[L]=x,lt._jQueryInterface};var ct="collapse",ht="bs.collapse",ut="."+ht,ft=g.fn[ct],dt={toggle:!0,parent:""},gt={toggle:"boolean",parent:"(string|element)"},_t={SHOW:"show"+ut,SHOWN:"shown"+ut,HIDE:"hide"+ut,HIDDEN:"hidden"+ut,CLICK_DATA_API:"click"+ut+".data-api"},mt="show",pt="collapse",vt="collapsing",yt="collapsed",Et="width",Ct="height",Tt=".show, .collapsing",St='[data-toggle="collapse"]',bt=function(){function a(e,t){this._isTransitioning=!1,this._element=e,this._config=this._getConfig(t),this._triggerArray=[].slice.call(document.querySelectorAll('[data-toggle="collapse"][href="#'+e.id+'"],[data-toggle="collapse"][data-target="#'+e.id+'"]'));for(var n=[].slice.call(document.querySelectorAll(St)),i=0,o=n.length;i<o;i++){var r=n[i],s=_.getSelectorFromElement(r),a=[].slice.call(document.querySelectorAll(s)).filter(function(t){return t===e});null!==s&&0<a.length&&(this._selector=s,this._triggerArray.push(r))}this._parent=this._config.parent?this._getParent():null,this._config.parent||this._addAriaAndCollapsedClass(this._element,this._triggerArray),this._config.toggle&&this.toggle()}var t=a.prototype;return t.toggle=function(){g(this._element).hasClass(mt)?this.hide():this.show()},t.show=function(){var t,e,n=this;if(!this._isTransitioning&&!g(this._element).hasClass(mt)&&(this._parent&&0===(t=[].slice.call(this._parent.querySelectorAll(Tt)).filter(function(t){return"string"==typeof n._config.parent?t.getAttribute("data-parent")===n._config.parent:t.classList.contains(pt)})).length&&(t=null),!(t&&(e=g(t).not(this._selector).data(ht))&&e._isTransitioning))){var i=g.Event(_t.SHOW);if(g(this._element).trigger(i),!i.isDefaultPrevented()){t&&(a._jQueryInterface.call(g(t).not(this._selector),"hide"),e||g(t).data(ht,null));var o=this._getDimension();g(this._element).removeClass(pt).addClass(vt),this._element.style[o]=0,this._triggerArray.length&&g(this._triggerArray).removeClass(yt).attr("aria-expanded",!0),this.setTransitioning(!0);var r="scroll"+(o[0].toUpperCase()+o.slice(1)),s=_.getTransitionDurationFromElement(this._element);g(this._element).one(_.TRANSITION_END,function(){g(n._element).removeClass(vt).addClass(pt).addClass(mt),n._element.style[o]="",n.setTransitioning(!1),g(n._element).trigger(_t.SHOWN)}).emulateTransitionEnd(s),this._element.style[o]=this._element[r]+"px"}}},t.hide=function(){var t=this;if(!this._isTransitioning&&g(this._element).hasClass(mt)){var e=g.Event(_t.HIDE);if(g(this._element).trigger(e),!e.isDefaultPrevented()){var n=this._getDimension();this._element.style[n]=this._element.getBoundingClientRect()[n]+"px",_.reflow(this._element),g(this._element).addClass(vt).removeClass(pt).removeClass(mt);var i=this._triggerArray.length;if(0<i)for(var o=0;o<i;o++){var r=this._triggerArray[o],s=_.getSelectorFromElement(r);if(null!==s)g([].slice.call(document.querySelectorAll(s))).hasClass(mt)||g(r).addClass(yt).attr("aria-expanded",!1)}this.setTransitioning(!0);this._element.style[n]="";var a=_.getTransitionDurationFromElement(this._element);g(this._element).one(_.TRANSITION_END,function(){t.setTransitioning(!1),g(t._element).removeClass(vt).addClass(pt).trigger(_t.HIDDEN)}).emulateTransitionEnd(a)}}},t.setTransitioning=function(t){this._isTransitioning=t},t.dispose=function(){g.removeData(this._element,ht),this._config=null,this._parent=null,this._element=null,this._triggerArray=null,this._isTransitioning=null},t._getConfig=function(t){return(t=l({},dt,t)).toggle=Boolean(t.toggle),_.typeCheckConfig(ct,t,gt),t},t._getDimension=function(){return g(this._element).hasClass(Et)?Et:Ct},t._getParent=function(){var t,n=this;_.isElement(this._config.parent)?(t=this._config.parent,"undefined"!=typeof this._config.parent.jquery&&(t=this._config.parent[0])):t=document.querySelector(this._config.parent);var e='[data-toggle="collapse"][data-parent="'+this._config.parent+'"]',i=[].slice.call(t.querySelectorAll(e));return g(i).each(function(t,e){n._addAriaAndCollapsedClass(a._getTargetFromElement(e),[e])}),t},t._addAriaAndCollapsedClass=function(t,e){var n=g(t).hasClass(mt);e.length&&g(e).toggleClass(yt,!n).attr("aria-expanded",n)},a._getTargetFromElement=function(t){var e=_.getSelectorFromElement(t);return e?document.querySelector(e):null},a._jQueryInterface=function(i){return this.each(function(){var t=g(this),e=t.data(ht),n=l({},dt,t.data(),"object"==typeof i&&i?i:{});if(!e&&n.toggle&&/show|hide/.test(i)&&(n.toggle=!1),e||(e=new a(this,n),t.data(ht,e)),"string"==typeof i){if("undefined"==typeof e[i])throw new TypeError('No method named "'+i+'"');e[i]()}})},s(a,null,[{key:"VERSION",get:function(){return"4.3.1"}},{key:"Default",get:function(){return dt}}]),a}();g(document).on(_t.CLICK_DATA_API,St,function(t){"A"===t.currentTarget.tagName&&t.preventDefault();var n=g(this),e=_.getSelectorFromElement(this),i=[].slice.call(document.querySelectorAll(e));g(i).each(function(){var t=g(this),e=t.data(ht)?"toggle":n.data();bt._jQueryInterface.call(t,e)})}),g.fn[ct]=bt._jQueryInterface,g.fn[ct].Constructor=bt,g.fn[ct].noConflict=function(){return g.fn[ct]=ft,bt._jQueryInterface};var It="dropdown",Dt="bs.dropdown",wt="."+Dt,At=".data-api",Nt=g.fn[It],Ot=new RegExp("38|40|27"),kt={HIDE:"hide"+wt,HIDDEN:"hidden"+wt,SHOW:"show"+wt,SHOWN:"shown"+wt,CLICK:"click"+wt,CLICK_DATA_API:"click"+wt+At,KEYDOWN_DATA_API:"keydown"+wt+At,KEYUP_DATA_API:"keyup"+wt+At},Pt="disabled",Lt="show",jt="dropup",Ht="dropright",Rt="dropleft",xt="dropdown-menu-right",Ft="position-static",Ut='[data-toggle="dropdown"]',Wt=".dropdown form",qt=".dropdown-menu",Mt=".navbar-nav",Kt=".dropdown-menu .dropdown-item:not(.disabled):not(:disabled)",Qt="top-start",Bt="top-end",Vt="bottom-start",Yt="bottom-end",zt="right-start",Xt="left-start",$t={offset:0,flip:!0,boundary:"scrollParent",reference:"toggle",display:"dynamic"},Gt={offset:"(number|string|function)",flip:"boolean",boundary:"(string|element)",reference:"(string|element)",display:"string"},Jt=function(){function c(t,e){this._element=t,this._popper=null,this._config=this._getConfig(e),this._menu=this._getMenuElement(),this._inNavbar=this._detectNavbar(),this._addEventListeners()}var t=c.prototype;return t.toggle=function(){if(!this._element.disabled&&!g(this._element).hasClass(Pt)){var t=c._getParentFromElement(this._element),e=g(this._menu).hasClass(Lt);if(c._clearMenus(),!e){var n={relatedTarget:this._element},i=g.Event(kt.SHOW,n);if(g(t).trigger(i),!i.isDefaultPrevented()){if(!this._inNavbar){if("undefined"==typeof u)throw new TypeError("Bootstrap's dropdowns require Popper.js (https://popper.js.org/)");var o=this._element;"parent"===this._config.reference?o=t:_.isElement(this._config.reference)&&(o=this._config.reference,"undefined"!=typeof this._config.reference.jquery&&(o=this._config.reference[0])),"scrollParent"!==this._config.boundary&&g(t).addClass(Ft),this._popper=new u(o,this._menu,this._getPopperConfig())}"ontouchstart"in document.documentElement&&0===g(t).closest(Mt).length&&g(document.body).children().on("mouseover",null,g.noop),this._element.focus(),this._element.setAttribute("aria-expanded",!0),g(this._menu).toggleClass(Lt),g(t).toggleClass(Lt).trigger(g.Event(kt.SHOWN,n))}}}},t.show=function(){if(!(this._element.disabled||g(this._element).hasClass(Pt)||g(this._menu).hasClass(Lt))){var t={relatedTarget:this._element},e=g.Event(kt.SHOW,t),n=c._getParentFromElement(this._element);g(n).trigger(e),e.isDefaultPrevented()||(g(this._menu).toggleClass(Lt),g(n).toggleClass(Lt).trigger(g.Event(kt.SHOWN,t)))}},t.hide=function(){if(!this._element.disabled&&!g(this._element).hasClass(Pt)&&g(this._menu).hasClass(Lt)){var t={relatedTarget:this._element},e=g.Event(kt.HIDE,t),n=c._getParentFromElement(this._element);g(n).trigger(e),e.isDefaultPrevented()||(g(this._menu).toggleClass(Lt),g(n).toggleClass(Lt).trigger(g.Event(kt.HIDDEN,t)))}},t.dispose=function(){g.removeData(this._element,Dt),g(this._element).off(wt),this._element=null,(this._menu=null)!==this._popper&&(this._popper.destroy(),this._popper=null)},t.update=function(){this._inNavbar=this._detectNavbar(),null!==this._popper&&this._popper.scheduleUpdate()},t._addEventListeners=function(){var e=this;g(this._element).on(kt.CLICK,function(t){t.preventDefault(),t.stopPropagation(),e.toggle()})},t._getConfig=function(t){return t=l({},this.constructor.Default,g(this._element).data(),t),_.typeCheckConfig(It,t,this.constructor.DefaultType),t},t._getMenuElement=function(){if(!this._menu){var t=c._getParentFromElement(this._element);t&&(this._menu=t.querySelector(qt))}return this._menu},t._getPlacement=function(){var t=g(this._element.parentNode),e=Vt;return t.hasClass(jt)?(e=Qt,g(this._menu).hasClass(xt)&&(e=Bt)):t.hasClass(Ht)?e=zt:t.hasClass(Rt)?e=Xt:g(this._menu).hasClass(xt)&&(e=Yt),e},t._detectNavbar=function(){return 0<g(this._element).closest(".navbar").length},t._getOffset=function(){var e=this,t={};return"function"==typeof this._config.offset?t.fn=function(t){return t.offsets=l({},t.offsets,e._config.offset(t.offsets,e._element)||{}),t}:t.offset=this._config.offset,t},t._getPopperConfig=function(){var t={placement:this._getPlacement(),modifiers:{offset:this._getOffset(),flip:{enabled:this._config.flip},preventOverflow:{boundariesElement:this._config.boundary}}};return"static"===this._config.display&&(t.modifiers.applyStyle={enabled:!1}),t},c._jQueryInterface=function(e){return this.each(function(){var t=g(this).data(Dt);if(t||(t=new c(this,"object"==typeof e?e:null),g(this).data(Dt,t)),"string"==typeof e){if("undefined"==typeof t[e])throw new TypeError('No method named "'+e+'"');t[e]()}})},c._clearMenus=function(t){if(!t||3!==t.which&&("keyup"!==t.type||9===t.which))for(var e=[].slice.call(document.querySelectorAll(Ut)),n=0,i=e.length;n<i;n++){var o=c._getParentFromElement(e[n]),r=g(e[n]).data(Dt),s={relatedTarget:e[n]};if(t&&"click"===t.type&&(s.clickEvent=t),r){var a=r._menu;if(g(o).hasClass(Lt)&&!(t&&("click"===t.type&&/input|textarea/i.test(t.target.tagName)||"keyup"===t.type&&9===t.which)&&g.contains(o,t.target))){var l=g.Event(kt.HIDE,s);g(o).trigger(l),l.isDefaultPrevented()||("ontouchstart"in document.documentElement&&g(document.body).children().off("mouseover",null,g.noop),e[n].setAttribute("aria-expanded","false"),g(a).removeClass(Lt),g(o).removeClass(Lt).trigger(g.Event(kt.HIDDEN,s)))}}}},c._getParentFromElement=function(t){var e,n=_.getSelectorFromElement(t);return n&&(e=document.querySelector(n)),e||t.parentNode},c._dataApiKeydownHandler=function(t){if((/input|textarea/i.test(t.target.tagName)?!(32===t.which||27!==t.which&&(40!==t.which&&38!==t.which||g(t.target).closest(qt).length)):Ot.test(t.which))&&(t.preventDefault(),t.stopPropagation(),!this.disabled&&!g(this).hasClass(Pt))){var e=c._getParentFromElement(this),n=g(e).hasClass(Lt);if(n&&(!n||27!==t.which&&32!==t.which)){var i=[].slice.call(e.querySelectorAll(Kt));if(0!==i.length){var o=i.indexOf(t.target);38===t.which&&0<o&&o--,40===t.which&&o<i.length-1&&o++,o<0&&(o=0),i[o].focus()}}else{if(27===t.which){var r=e.querySelector(Ut);g(r).trigger("focus")}g(this).trigger("click")}}},s(c,null,[{key:"VERSION",get:function(){return"4.3.1"}},{key:"Default",get:function(){return $t}},{key:"DefaultType",get:function(){return Gt}}]),c}();g(document).on(kt.KEYDOWN_DATA_API,Ut,Jt._dataApiKeydownHandler).on(kt.KEYDOWN_DATA_API,qt,Jt._dataApiKeydownHandler).on(kt.CLICK_DATA_API+" "+kt.KEYUP_DATA_API,Jt._clearMenus).on(kt.CLICK_DATA_API,Ut,function(t){t.preventDefault(),t.stopPropagation(),Jt._jQueryInterface.call(g(this),"toggle")}).on(kt.CLICK_DATA_API,Wt,function(t){t.stopPropagation()}),g.fn[It]=Jt._jQueryInterface,g.fn[It].Constructor=Jt,g.fn[It].noConflict=function(){return g.fn[It]=Nt,Jt._jQueryInterface};var Zt="modal",te="bs.modal",ee="."+te,ne=g.fn[Zt],ie={backdrop:!0,keyboard:!0,focus:!0,show:!0},oe={backdrop:"(boolean|string)",keyboard:"boolean",focus:"boolean",show:"boolean"},re={HIDE:"hide"+ee,HIDDEN:"hidden"+ee,SHOW:"show"+ee,SHOWN:"shown"+ee,FOCUSIN:"focusin"+ee,RESIZE:"resize"+ee,CLICK_DISMISS:"click.dismiss"+ee,KEYDOWN_DISMISS:"keydown.dismiss"+ee,MOUSEUP_DISMISS:"mouseup.dismiss"+ee,MOUSEDOWN_DISMISS:"mousedown.dismiss"+ee,CLICK_DATA_API:"click"+ee+".data-api"},se="modal-dialog-scrollable",ae="modal-scrollbar-measure",le="modal-backdrop",ce="modal-open",he="fade",ue="show",fe=".modal-dialog",de=".modal-body",ge='[data-toggle="modal"]',_e='[data-dismiss="modal"]',me=".fixed-top, .fixed-bottom, .is-fixed, .sticky-top",pe=".sticky-top",ve=function(){function o(t,e){this._config=this._getConfig(e),this._element=t,this._dialog=t.querySelector(fe),this._backdrop=null,this._isShown=!1,this._isBodyOverflowing=!1,this._ignoreBackdropClick=!1,this._isTransitioning=!1,this._scrollbarWidth=0}var t=o.prototype;return t.toggle=function(t){return this._isShown?this.hide():this.show(t)},t.show=function(t){var e=this;if(!this._isShown&&!this._isTransitioning){g(this._element).hasClass(he)&&(this._isTransitioning=!0);var n=g.Event(re.SHOW,{relatedTarget:t});g(this._element).trigger(n),this._isShown||n.isDefaultPrevented()||(this._isShown=!0,this._checkScrollbar(),this._setScrollbar(),this._adjustDialog(),this._setEscapeEvent(),this._setResizeEvent(),g(this._element).on(re.CLICK_DISMISS,_e,function(t){return e.hide(t)}),g(this._dialog).on(re.MOUSEDOWN_DISMISS,function(){g(e._element).one(re.MOUSEUP_DISMISS,function(t){g(t.target).is(e._element)&&(e._ignoreBackdropClick=!0)})}),this._showBackdrop(function(){return e._showElement(t)}))}},t.hide=function(t){var e=this;if(t&&t.preventDefault(),this._isShown&&!this._isTransitioning){var n=g.Event(re.HIDE);if(g(this._element).trigger(n),this._isShown&&!n.isDefaultPrevented()){this._isShown=!1;var i=g(this._element).hasClass(he);if(i&&(this._isTransitioning=!0),this._setEscapeEvent(),this._setResizeEvent(),g(document).off(re.FOCUSIN),g(this._element).removeClass(ue),g(this._element).off(re.CLICK_DISMISS),g(this._dialog).off(re.MOUSEDOWN_DISMISS),i){var o=_.getTransitionDurationFromElement(this._element);g(this._element).one(_.TRANSITION_END,function(t){return e._hideModal(t)}).emulateTransitionEnd(o)}else this._hideModal()}}},t.dispose=function(){[window,this._element,this._dialog].forEach(function(t){return g(t).off(ee)}),g(document).off(re.FOCUSIN),g.removeData(this._element,te),this._config=null,this._element=null,this._dialog=null,this._backdrop=null,this._isShown=null,this._isBodyOverflowing=null,this._ignoreBackdropClick=null,this._isTransitioning=null,this._scrollbarWidth=null},t.handleUpdate=function(){this._adjustDialog()},t._getConfig=function(t){return t=l({},ie,t),_.typeCheckConfig(Zt,t,oe),t},t._showElement=function(t){var e=this,n=g(this._element).hasClass(he);this._element.parentNode&&this._element.parentNode.nodeType===Node.ELEMENT_NODE||document.body.appendChild(this._element),this._element.style.display="block",this._element.removeAttribute("aria-hidden"),this._element.setAttribute("aria-modal",!0),g(this._dialog).hasClass(se)?this._dialog.querySelector(de).scrollTop=0:this._element.scrollTop=0,n&&_.reflow(this._element),g(this._element).addClass(ue),this._config.focus&&this._enforceFocus();var i=g.Event(re.SHOWN,{relatedTarget:t}),o=function(){e._config.focus&&e._element.focus(),e._isTransitioning=!1,g(e._element).trigger(i)};if(n){var r=_.getTransitionDurationFromElement(this._dialog);g(this._dialog).one(_.TRANSITION_END,o).emulateTransitionEnd(r)}else o()},t._enforceFocus=function(){var e=this;g(document).off(re.FOCUSIN).on(re.FOCUSIN,function(t){document!==t.target&&e._element!==t.target&&0===g(e._element).has(t.target).length&&e._element.focus()})},t._setEscapeEvent=function(){var e=this;this._isShown&&this._config.keyboard?g(this._element).on(re.KEYDOWN_DISMISS,function(t){27===t.which&&(t.preventDefault(),e.hide())}):this._isShown||g(this._element).off(re.KEYDOWN_DISMISS)},t._setResizeEvent=function(){var e=this;this._isShown?g(window).on(re.RESIZE,function(t){return e.handleUpdate(t)}):g(window).off(re.RESIZE)},t._hideModal=function(){var t=this;this._element.style.display="none",this._element.setAttribute("aria-hidden",!0),this._element.removeAttribute("aria-modal"),this._isTransitioning=!1,this._showBackdrop(function(){g(document.body).removeClass(ce),t._resetAdjustments(),t._resetScrollbar(),g(t._element).trigger(re.HIDDEN)})},t._removeBackdrop=function(){this._backdrop&&(g(this._backdrop).remove(),this._backdrop=null)},t._showBackdrop=function(t){var e=this,n=g(this._element).hasClass(he)?he:"";if(this._isShown&&this._config.backdrop){if(this._backdrop=document.createElement("div"),this._backdrop.className=le,n&&this._backdrop.classList.add(n),g(this._backdrop).appendTo(document.body),g(this._element).on(re.CLICK_DISMISS,function(t){e._ignoreBackdropClick?e._ignoreBackdropClick=!1:t.target===t.currentTarget&&("static"===e._config.backdrop?e._element.focus():e.hide())}),n&&_.reflow(this._backdrop),g(this._backdrop).addClass(ue),!t)return;if(!n)return void t();var i=_.getTransitionDurationFromElement(this._backdrop);g(this._backdrop).one(_.TRANSITION_END,t).emulateTransitionEnd(i)}else if(!this._isShown&&this._backdrop){g(this._backdrop).removeClass(ue);var o=function(){e._removeBackdrop(),t&&t()};if(g(this._element).hasClass(he)){var r=_.getTransitionDurationFromElement(this._backdrop);g(this._backdrop).one(_.TRANSITION_END,o).emulateTransitionEnd(r)}else o()}else t&&t()},t._adjustDialog=function(){var t=this._element.scrollHeight>document.documentElement.clientHeight;!this._isBodyOverflowing&&t&&(this._element.style.paddingLeft=this._scrollbarWidth+"px"),this._isBodyOverflowing&&!t&&(this._element.style.paddingRight=this._scrollbarWidth+"px")},t._resetAdjustments=function(){this._element.style.paddingLeft="",this._element.style.paddingRight=""},t._checkScrollbar=function(){var t=document.body.getBoundingClientRect();this._isBodyOverflowing=t.left+t.right<window.innerWidth,this._scrollbarWidth=this._getScrollbarWidth()},t._setScrollbar=function(){var o=this;if(this._isBodyOverflowing){var t=[].slice.call(document.querySelectorAll(me)),e=[].slice.call(document.querySelectorAll(pe));g(t).each(function(t,e){var n=e.style.paddingRight,i=g(e).css("padding-right");g(e).data("padding-right",n).css("padding-right",parseFloat(i)+o._scrollbarWidth+"px")}),g(e).each(function(t,e){var n=e.style.marginRight,i=g(e).css("margin-right");g(e).data("margin-right",n).css("margin-right",parseFloat(i)-o._scrollbarWidth+"px")});var n=document.body.style.paddingRight,i=g(document.body).css("padding-right");g(document.body).data("padding-right",n).css("padding-right",parseFloat(i)+this._scrollbarWidth+"px")}g(document.body).addClass(ce)},t._resetScrollbar=function(){var t=[].slice.call(document.querySelectorAll(me));g(t).each(function(t,e){var n=g(e).data("padding-right");g(e).removeData("padding-right"),e.style.paddingRight=n||""});var e=[].slice.call(document.querySelectorAll(""+pe));g(e).each(function(t,e){var n=g(e).data("margin-right");"undefined"!=typeof n&&g(e).css("margin-right",n).removeData("margin-right")});var n=g(document.body).data("padding-right");g(document.body).removeData("padding-right"),document.body.style.paddingRight=n||""},t._getScrollbarWidth=function(){var t=document.createElement("div");t.className=ae,document.body.appendChild(t);var e=t.getBoundingClientRect().width-t.clientWidth;return document.body.removeChild(t),e},o._jQueryInterface=function(n,i){return this.each(function(){var t=g(this).data(te),e=l({},ie,g(this).data(),"object"==typeof n&&n?n:{});if(t||(t=new o(this,e),g(this).data(te,t)),"string"==typeof n){if("undefined"==typeof t[n])throw new TypeError('No method named "'+n+'"');t[n](i)}else e.show&&t.show(i)})},s(o,null,[{key:"VERSION",get:function(){return"4.3.1"}},{key:"Default",get:function(){return ie}}]),o}();g(document).on(re.CLICK_DATA_API,ge,function(t){var e,n=this,i=_.getSelectorFromElement(this);i&&(e=document.querySelector(i));var o=g(e).data(te)?"toggle":l({},g(e).data(),g(this).data());"A"!==this.tagName&&"AREA"!==this.tagName||t.preventDefault();var r=g(e).one(re.SHOW,function(t){t.isDefaultPrevented()||r.one(re.HIDDEN,function(){g(n).is(":visible")&&n.focus()})});ve._jQueryInterface.call(g(e),o,this)}),g.fn[Zt]=ve._jQueryInterface,g.fn[Zt].Constructor=ve,g.fn[Zt].noConflict=function(){return g.fn[Zt]=ne,ve._jQueryInterface};var ye=["background","cite","href","itemtype","longdesc","poster","src","xlink:href"],Ee={"*":["class","dir","id","lang","role",/^aria-[\w-]*$/i],a:["target","href","title","rel"],area:[],b:[],br:[],col:[],code:[],div:[],em:[],hr:[],h1:[],h2:[],h3:[],h4:[],h5:[],h6:[],i:[],img:["src","alt","title","width","height"],li:[],ol:[],p:[],pre:[],s:[],small:[],span:[],sub:[],sup:[],strong:[],u:[],ul:[]},Ce=/^(?:(?:https?|mailto|ftp|tel|file):|[^&:/?#]*(?:[/?#]|$))/gi,Te=/^data:(?:image\/(?:bmp|gif|jpeg|jpg|png|tiff|webp)|video\/(?:mpeg|mp4|ogg|webm)|audio\/(?:mp3|oga|ogg|opus));base64,[a-z0-9+/]+=*$/i;function Se(t,s,e){if(0===t.length)return t;if(e&&"function"==typeof e)return e(t);for(var n=(new window.DOMParser).parseFromString(t,"text/html"),a=Object.keys(s),l=[].slice.call(n.body.querySelectorAll("*")),i=function(t,e){var n=l[t],i=n.nodeName.toLowerCase();if(-1===a.indexOf(n.nodeName.toLowerCase()))return n.parentNode.removeChild(n),"continue";var o=[].slice.call(n.attributes),r=[].concat(s["*"]||[],s[i]||[]);o.forEach(function(t){(function(t,e){var n=t.nodeName.toLowerCase();if(-1!==e.indexOf(n))return-1===ye.indexOf(n)||Boolean(t.nodeValue.match(Ce)||t.nodeValue.match(Te));for(var i=e.filter(function(t){return t instanceof RegExp}),o=0,r=i.length;o<r;o++)if(n.match(i[o]))return!0;return!1})(t,r)||n.removeAttribute(t.nodeName)})},o=0,r=l.length;o<r;o++)i(o);return n.body.innerHTML}var be="tooltip",Ie="bs.tooltip",De="."+Ie,we=g.fn[be],Ae="bs-tooltip",Ne=new RegExp("(^|\\s)"+Ae+"\\S+","g"),Oe=["sanitize","whiteList","sanitizeFn"],ke={animation:"boolean",template:"string",title:"(string|element|function)",trigger:"string",delay:"(number|object)",html:"boolean",selector:"(string|boolean)",placement:"(string|function)",offset:"(number|string|function)",container:"(string|element|boolean)",fallbackPlacement:"(string|array)",boundary:"(string|element)",sanitize:"boolean",sanitizeFn:"(null|function)",whiteList:"object"},Pe={AUTO:"auto",TOP:"top",RIGHT:"right",BOTTOM:"bottom",LEFT:"left"},Le={animation:!0,template:'<div class="tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>',trigger:"hover focus",title:"",delay:0,html:!1,selector:!1,placement:"top",offset:0,container:!1,fallbackPlacement:"flip",boundary:"scrollParent",sanitize:!0,sanitizeFn:null,whiteList:Ee},je="show",He="out",Re={HIDE:"hide"+De,HIDDEN:"hidden"+De,SHOW:"show"+De,SHOWN:"shown"+De,INSERTED:"inserted"+De,CLICK:"click"+De,FOCUSIN:"focusin"+De,FOCUSOUT:"focusout"+De,MOUSEENTER:"mouseenter"+De,MOUSELEAVE:"mouseleave"+De},xe="fade",Fe="show",Ue=".tooltip-inner",We=".arrow",qe="hover",Me="focus",Ke="click",Qe="manual",Be=function(){function i(t,e){if("undefined"==typeof u)throw new TypeError("Bootstrap's tooltips require Popper.js (https://popper.js.org/)");this._isEnabled=!0,this._timeout=0,this._hoverState="",this._activeTrigger={},this._popper=null,this.element=t,this.config=this._getConfig(e),this.tip=null,this._setListeners()}var t=i.prototype;return t.enable=function(){this._isEnabled=!0},t.disable=function(){this._isEnabled=!1},t.toggleEnabled=function(){this._isEnabled=!this._isEnabled},t.toggle=function(t){if(this._isEnabled)if(t){var e=this.constructor.DATA_KEY,n=g(t.currentTarget).data(e);n||(n=new this.constructor(t.currentTarget,this._getDelegateConfig()),g(t.currentTarget).data(e,n)),n._activeTrigger.click=!n._activeTrigger.click,n._isWithActiveTrigger()?n._enter(null,n):n._leave(null,n)}else{if(g(this.getTipElement()).hasClass(Fe))return void this._leave(null,this);this._enter(null,this)}},t.dispose=function(){clearTimeout(this._timeout),g.removeData(this.element,this.constructor.DATA_KEY),g(this.element).off(this.constructor.EVENT_KEY),g(this.element).closest(".modal").off("hide.bs.modal"),this.tip&&g(this.tip).remove(),this._isEnabled=null,this._timeout=null,this._hoverState=null,(this._activeTrigger=null)!==this._popper&&this._popper.destroy(),this._popper=null,this.element=null,this.config=null,this.tip=null},t.show=function(){var e=this;if("none"===g(this.element).css("display"))throw new Error("Please use show on visible elements");var t=g.Event(this.constructor.Event.SHOW);if(this.isWithContent()&&this._isEnabled){g(this.element).trigger(t);var n=_.findShadowRoot(this.element),i=g.contains(null!==n?n:this.element.ownerDocument.documentElement,this.element);if(t.isDefaultPrevented()||!i)return;var o=this.getTipElement(),r=_.getUID(this.constructor.NAME);o.setAttribute("id",r),this.element.setAttribute("aria-describedby",r),this.setContent(),this.config.animation&&g(o).addClass(xe);var s="function"==typeof this.config.placement?this.config.placement.call(this,o,this.element):this.config.placement,a=this._getAttachment(s);this.addAttachmentClass(a);var l=this._getContainer();g(o).data(this.constructor.DATA_KEY,this),g.contains(this.element.ownerDocument.documentElement,this.tip)||g(o).appendTo(l),g(this.element).trigger(this.constructor.Event.INSERTED),this._popper=new u(this.element,o,{placement:a,modifiers:{offset:this._getOffset(),flip:{behavior:this.config.fallbackPlacement},arrow:{element:We},preventOverflow:{boundariesElement:this.config.boundary}},onCreate:function(t){t.originalPlacement!==t.placement&&e._handlePopperPlacementChange(t)},onUpdate:function(t){return e._handlePopperPlacementChange(t)}}),g(o).addClass(Fe),"ontouchstart"in document.documentElement&&g(document.body).children().on("mouseover",null,g.noop);var c=function(){e.config.animation&&e._fixTransition();var t=e._hoverState;e._hoverState=null,g(e.element).trigger(e.constructor.Event.SHOWN),t===He&&e._leave(null,e)};if(g(this.tip).hasClass(xe)){var h=_.getTransitionDurationFromElement(this.tip);g(this.tip).one(_.TRANSITION_END,c).emulateTransitionEnd(h)}else c()}},t.hide=function(t){var e=this,n=this.getTipElement(),i=g.Event(this.constructor.Event.HIDE),o=function(){e._hoverState!==je&&n.parentNode&&n.parentNode.removeChild(n),e._cleanTipClass(),e.element.removeAttribute("aria-describedby"),g(e.element).trigger(e.constructor.Event.HIDDEN),null!==e._popper&&e._popper.destroy(),t&&t()};if(g(this.element).trigger(i),!i.isDefaultPrevented()){if(g(n).removeClass(Fe),"ontouchstart"in document.documentElement&&g(document.body).children().off("mouseover",null,g.noop),this._activeTrigger[Ke]=!1,this._activeTrigger[Me]=!1,this._activeTrigger[qe]=!1,g(this.tip).hasClass(xe)){var r=_.getTransitionDurationFromElement(n);g(n).one(_.TRANSITION_END,o).emulateTransitionEnd(r)}else o();this._hoverState=""}},t.update=function(){null!==this._popper&&this._popper.scheduleUpdate()},t.isWithContent=function(){return Boolean(this.getTitle())},t.addAttachmentClass=function(t){g(this.getTipElement()).addClass(Ae+"-"+t)},t.getTipElement=function(){return this.tip=this.tip||g(this.config.template)[0],this.tip},t.setContent=function(){var t=this.getTipElement();this.setElementContent(g(t.querySelectorAll(Ue)),this.getTitle()),g(t).removeClass(xe+" "+Fe)},t.setElementContent=function(t,e){"object"!=typeof e||!e.nodeType&&!e.jquery?this.config.html?(this.config.sanitize&&(e=Se(e,this.config.whiteList,this.config.sanitizeFn)),t.html(e)):t.text(e):this.config.html?g(e).parent().is(t)||t.empty().append(e):t.text(g(e).text())},t.getTitle=function(){var t=this.element.getAttribute("data-original-title");return t||(t="function"==typeof this.config.title?this.config.title.call(this.element):this.config.title),t},t._getOffset=function(){var e=this,t={};return"function"==typeof this.config.offset?t.fn=function(t){return t.offsets=l({},t.offsets,e.config.offset(t.offsets,e.element)||{}),t}:t.offset=this.config.offset,t},t._getContainer=function(){return!1===this.config.container?document.body:_.isElement(this.config.container)?g(this.config.container):g(document).find(this.config.container)},t._getAttachment=function(t){return Pe[t.toUpperCase()]},t._setListeners=function(){var i=this;this.config.trigger.split(" ").forEach(function(t){if("click"===t)g(i.element).on(i.constructor.Event.CLICK,i.config.selector,function(t){return i.toggle(t)});else if(t!==Qe){var e=t===qe?i.constructor.Event.MOUSEENTER:i.constructor.Event.FOCUSIN,n=t===qe?i.constructor.Event.MOUSELEAVE:i.constructor.Event.FOCUSOUT;g(i.element).on(e,i.config.selector,function(t){return i._enter(t)}).on(n,i.config.selector,function(t){return i._leave(t)})}}),g(this.element).closest(".modal").on("hide.bs.modal",function(){i.element&&i.hide()}),this.config.selector?this.config=l({},this.config,{trigger:"manual",selector:""}):this._fixTitle()},t._fixTitle=function(){var t=typeof this.element.getAttribute("data-original-title");(this.element.getAttribute("title")||"string"!==t)&&(this.element.setAttribute("data-original-title",this.element.getAttribute("title")||""),this.element.setAttribute("title",""))},t._enter=function(t,e){var n=this.constructor.DATA_KEY;(e=e||g(t.currentTarget).data(n))||(e=new this.constructor(t.currentTarget,this._getDelegateConfig()),g(t.currentTarget).data(n,e)),t&&(e._activeTrigger["focusin"===t.type?Me:qe]=!0),g(e.getTipElement()).hasClass(Fe)||e._hoverState===je?e._hoverState=je:(clearTimeout(e._timeout),e._hoverState=je,e.config.delay&&e.config.delay.show?e._timeout=setTimeout(function(){e._hoverState===je&&e.show()},e.config.delay.show):e.show())},t._leave=function(t,e){var n=this.constructor.DATA_KEY;(e=e||g(t.currentTarget).data(n))||(e=new this.constructor(t.currentTarget,this._getDelegateConfig()),g(t.currentTarget).data(n,e)),t&&(e._activeTrigger["focusout"===t.type?Me:qe]=!1),e._isWithActiveTrigger()||(clearTimeout(e._timeout),e._hoverState=He,e.config.delay&&e.config.delay.hide?e._timeout=setTimeout(function(){e._hoverState===He&&e.hide()},e.config.delay.hide):e.hide())},t._isWithActiveTrigger=function(){for(var t in this._activeTrigger)if(this._activeTrigger[t])return!0;return!1},t._getConfig=function(t){var e=g(this.element).data();return Object.keys(e).forEach(function(t){-1!==Oe.indexOf(t)&&delete e[t]}),"number"==typeof(t=l({},this.constructor.Default,e,"object"==typeof t&&t?t:{})).delay&&(t.delay={show:t.delay,hide:t.delay}),"number"==typeof t.title&&(t.title=t.title.toString()),"number"==typeof t.content&&(t.content=t.content.toString()),_.typeCheckConfig(be,t,this.constructor.DefaultType),t.sanitize&&(t.template=Se(t.template,t.whiteList,t.sanitizeFn)),t},t._getDelegateConfig=function(){var t={};if(this.config)for(var e in this.config)this.constructor.Default[e]!==this.config[e]&&(t[e]=this.config[e]);return t},t._cleanTipClass=function(){var t=g(this.getTipElement()),e=t.attr("class").match(Ne);null!==e&&e.length&&t.removeClass(e.join(""))},t._handlePopperPlacementChange=function(t){var e=t.instance;this.tip=e.popper,this._cleanTipClass(),this.addAttachmentClass(this._getAttachment(t.placement))},t._fixTransition=function(){var t=this.getTipElement(),e=this.config.animation;null===t.getAttribute("x-placement")&&(g(t).removeClass(xe),this.config.animation=!1,this.hide(),this.show(),this.config.animation=e)},i._jQueryInterface=function(n){return this.each(function(){var t=g(this).data(Ie),e="object"==typeof n&&n;if((t||!/dispose|hide/.test(n))&&(t||(t=new i(this,e),g(this).data(Ie,t)),"string"==typeof n)){if("undefined"==typeof t[n])throw new TypeError('No method named "'+n+'"');t[n]()}})},s(i,null,[{key:"VERSION",get:function(){return"4.3.1"}},{key:"Default",get:function(){return Le}},{key:"NAME",get:function(){return be}},{key:"DATA_KEY",get:function(){return Ie}},{key:"Event",get:function(){return Re}},{key:"EVENT_KEY",get:function(){return De}},{key:"DefaultType",get:function(){return ke}}]),i}();g.fn[be]=Be._jQueryInterface,g.fn[be].Constructor=Be,g.fn[be].noConflict=function(){return g.fn[be]=we,Be._jQueryInterface};var Ve="popover",Ye="bs.popover",ze="."+Ye,Xe=g.fn[Ve],$e="bs-popover",Ge=new RegExp("(^|\\s)"+$e+"\\S+","g"),Je=l({},Be.Default,{placement:"right",trigger:"click",content:"",template:'<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'}),Ze=l({},Be.DefaultType,{content:"(string|element|function)"}),tn="fade",en="show",nn=".popover-header",on=".popover-body",rn={HIDE:"hide"+ze,HIDDEN:"hidden"+ze,SHOW:"show"+ze,SHOWN:"shown"+ze,INSERTED:"inserted"+ze,CLICK:"click"+ze,FOCUSIN:"focusin"+ze,FOCUSOUT:"focusout"+ze,MOUSEENTER:"mouseenter"+ze,MOUSELEAVE:"mouseleave"+ze},sn=function(t){var e,n;function i(){return t.apply(this,arguments)||this}n=t,(e=i).prototype=Object.create(n.prototype),(e.prototype.constructor=e).__proto__=n;var o=i.prototype;return o.isWithContent=function(){return this.getTitle()||this._getContent()},o.addAttachmentClass=function(t){g(this.getTipElement()).addClass($e+"-"+t)},o.getTipElement=function(){return this.tip=this.tip||g(this.config.template)[0],this.tip},o.setContent=function(){var t=g(this.getTipElement());this.setElementContent(t.find(nn),this.getTitle());var e=this._getContent();"function"==typeof e&&(e=e.call(this.element)),this.setElementContent(t.find(on),e),t.removeClass(tn+" "+en)},o._getContent=function(){return this.element.getAttribute("data-content")||this.config.content},o._cleanTipClass=function(){var t=g(this.getTipElement()),e=t.attr("class").match(Ge);null!==e&&0<e.length&&t.removeClass(e.join(""))},i._jQueryInterface=function(n){return this.each(function(){var t=g(this).data(Ye),e="object"==typeof n?n:null;if((t||!/dispose|hide/.test(n))&&(t||(t=new i(this,e),g(this).data(Ye,t)),"string"==typeof n)){if("undefined"==typeof t[n])throw new TypeError('No method named "'+n+'"');t[n]()}})},s(i,null,[{key:"VERSION",get:function(){return"4.3.1"}},{key:"Default",get:function(){return Je}},{key:"NAME",get:function(){return Ve}},{key:"DATA_KEY",get:function(){return Ye}},{key:"Event",get:function(){return rn}},{key:"EVENT_KEY",get:function(){return ze}},{key:"DefaultType",get:function(){return Ze}}]),i}(Be);g.fn[Ve]=sn._jQueryInterface,g.fn[Ve].Constructor=sn,g.fn[Ve].noConflict=function(){return g.fn[Ve]=Xe,sn._jQueryInterface};var an="scrollspy",ln="bs.scrollspy",cn="."+ln,hn=g.fn[an],un={offset:10,method:"auto",target:""},fn={offset:"number",method:"string",target:"(string|element)"},dn={ACTIVATE:"activate"+cn,SCROLL:"scroll"+cn,LOAD_DATA_API:"load"+cn+".data-api"},gn="dropdown-item",_n="active",mn='[data-spy="scroll"]',pn=".nav, .list-group",vn=".nav-link",yn=".nav-item",En=".list-group-item",Cn=".dropdown",Tn=".dropdown-item",Sn=".dropdown-toggle",bn="offset",In="position",Dn=function(){function n(t,e){var n=this;this._element=t,this._scrollElement="BODY"===t.tagName?window:t,this._config=this._getConfig(e),this._selector=this._config.target+" "+vn+","+this._config.target+" "+En+","+this._config.target+" "+Tn,this._offsets=[],this._targets=[],this._activeTarget=null,this._scrollHeight=0,g(this._scrollElement).on(dn.SCROLL,function(t){return n._process(t)}),this.refresh(),this._process()}var t=n.prototype;return t.refresh=function(){var e=this,t=this._scrollElement===this._scrollElement.window?bn:In,o="auto"===this._config.method?t:this._config.method,r=o===In?this._getScrollTop():0;this._offsets=[],this._targets=[],this._scrollHeight=this._getScrollHeight(),[].slice.call(document.querySelectorAll(this._selector)).map(function(t){var e,n=_.getSelectorFromElement(t);if(n&&(e=document.querySelector(n)),e){var i=e.getBoundingClientRect();if(i.width||i.height)return[g(e)[o]().top+r,n]}return null}).filter(function(t){return t}).sort(function(t,e){return t[0]-e[0]}).forEach(function(t){e._offsets.push(t[0]),e._targets.push(t[1])})},t.dispose=function(){g.removeData(this._element,ln),g(this._scrollElement).off(cn),this._element=null,this._scrollElement=null,this._config=null,this._selector=null,this._offsets=null,this._targets=null,this._activeTarget=null,this._scrollHeight=null},t._getConfig=function(t){if("string"!=typeof(t=l({},un,"object"==typeof t&&t?t:{})).target){var e=g(t.target).attr("id");e||(e=_.getUID(an),g(t.target).attr("id",e)),t.target="#"+e}return _.typeCheckConfig(an,t,fn),t},t._getScrollTop=function(){return this._scrollElement===window?this._scrollElement.pageYOffset:this._scrollElement.scrollTop},t._getScrollHeight=function(){return this._scrollElement.scrollHeight||Math.max(document.body.scrollHeight,document.documentElement.scrollHeight)},t._getOffsetHeight=function(){return this._scrollElement===window?window.innerHeight:this._scrollElement.getBoundingClientRect().height},t._process=function(){var t=this._getScrollTop()+this._config.offset,e=this._getScrollHeight(),n=this._config.offset+e-this._getOffsetHeight();if(this._scrollHeight!==e&&this.refresh(),n<=t){var i=this._targets[this._targets.length-1];this._activeTarget!==i&&this._activate(i)}else{if(this._activeTarget&&t<this._offsets[0]&&0<this._offsets[0])return this._activeTarget=null,void this._clear();for(var o=this._offsets.length;o--;){this._activeTarget!==this._targets[o]&&t>=this._offsets[o]&&("undefined"==typeof this._offsets[o+1]||t<this._offsets[o+1])&&this._activate(this._targets[o])}}},t._activate=function(e){this._activeTarget=e,this._clear();var t=this._selector.split(",").map(function(t){return t+'[data-target="'+e+'"],'+t+'[href="'+e+'"]'}),n=g([].slice.call(document.querySelectorAll(t.join(","))));n.hasClass(gn)?(n.closest(Cn).find(Sn).addClass(_n),n.addClass(_n)):(n.addClass(_n),n.parents(pn).prev(vn+", "+En).addClass(_n),n.parents(pn).prev(yn).children(vn).addClass(_n)),g(this._scrollElement).trigger(dn.ACTIVATE,{relatedTarget:e})},t._clear=function(){[].slice.call(document.querySelectorAll(this._selector)).filter(function(t){return t.classList.contains(_n)}).forEach(function(t){return t.classList.remove(_n)})},n._jQueryInterface=function(e){return this.each(function(){var t=g(this).data(ln);if(t||(t=new n(this,"object"==typeof e&&e),g(this).data(ln,t)),"string"==typeof e){if("undefined"==typeof t[e])throw new TypeError('No method named "'+e+'"');t[e]()}})},s(n,null,[{key:"VERSION",get:function(){return"4.3.1"}},{key:"Default",get:function(){return un}}]),n}();g(window).on(dn.LOAD_DATA_API,function(){for(var t=[].slice.call(document.querySelectorAll(mn)),e=t.length;e--;){var n=g(t[e]);Dn._jQueryInterface.call(n,n.data())}}),g.fn[an]=Dn._jQueryInterface,g.fn[an].Constructor=Dn,g.fn[an].noConflict=function(){return g.fn[an]=hn,Dn._jQueryInterface};var wn="bs.tab",An="."+wn,Nn=g.fn.tab,On={HIDE:"hide"+An,HIDDEN:"hidden"+An,SHOW:"show"+An,SHOWN:"shown"+An,CLICK_DATA_API:"click"+An+".data-api"},kn="dropdown-menu",Pn="active",Ln="disabled",jn="fade",Hn="show",Rn=".dropdown",xn=".nav, .list-group",Fn=".active",Un="> li > .active",Wn='[data-toggle="tab"], [data-toggle="pill"], [data-toggle="list"]',qn=".dropdown-toggle",Mn="> .dropdown-menu .active",Kn=function(){function i(t){this._element=t}var t=i.prototype;return t.show=function(){var n=this;if(!(this._element.parentNode&&this._element.parentNode.nodeType===Node.ELEMENT_NODE&&g(this._element).hasClass(Pn)||g(this._element).hasClass(Ln))){var t,i,e=g(this._element).closest(xn)[0],o=_.getSelectorFromElement(this._element);if(e){var r="UL"===e.nodeName||"OL"===e.nodeName?Un:Fn;i=(i=g.makeArray(g(e).find(r)))[i.length-1]}var s=g.Event(On.HIDE,{relatedTarget:this._element}),a=g.Event(On.SHOW,{relatedTarget:i});if(i&&g(i).trigger(s),g(this._element).trigger(a),!a.isDefaultPrevented()&&!s.isDefaultPrevented()){o&&(t=document.querySelector(o)),this._activate(this._element,e);var l=function(){var t=g.Event(On.HIDDEN,{relatedTarget:n._element}),e=g.Event(On.SHOWN,{relatedTarget:i});g(i).trigger(t),g(n._element).trigger(e)};t?this._activate(t,t.parentNode,l):l()}}},t.dispose=function(){g.removeData(this._element,wn),this._element=null},t._activate=function(t,e,n){var i=this,o=(!e||"UL"!==e.nodeName&&"OL"!==e.nodeName?g(e).children(Fn):g(e).find(Un))[0],r=n&&o&&g(o).hasClass(jn),s=function(){return i._transitionComplete(t,o,n)};if(o&&r){var a=_.getTransitionDurationFromElement(o);g(o).removeClass(Hn).one(_.TRANSITION_END,s).emulateTransitionEnd(a)}else s()},t._transitionComplete=function(t,e,n){if(e){g(e).removeClass(Pn);var i=g(e.parentNode).find(Mn)[0];i&&g(i).removeClass(Pn),"tab"===e.getAttribute("role")&&e.setAttribute("aria-selected",!1)}if(g(t).addClass(Pn),"tab"===t.getAttribute("role")&&t.setAttribute("aria-selected",!0),_.reflow(t),t.classList.contains(jn)&&t.classList.add(Hn),t.parentNode&&g(t.parentNode).hasClass(kn)){var o=g(t).closest(Rn)[0];if(o){var r=[].slice.call(o.querySelectorAll(qn));g(r).addClass(Pn)}t.setAttribute("aria-expanded",!0)}n&&n()},i._jQueryInterface=function(n){return this.each(function(){var t=g(this),e=t.data(wn);if(e||(e=new i(this),t.data(wn,e)),"string"==typeof n){if("undefined"==typeof e[n])throw new TypeError('No method named "'+n+'"');e[n]()}})},s(i,null,[{key:"VERSION",get:function(){return"4.3.1"}}]),i}();g(document).on(On.CLICK_DATA_API,Wn,function(t){t.preventDefault(),Kn._jQueryInterface.call(g(this),"show")}),g.fn.tab=Kn._jQueryInterface,g.fn.tab.Constructor=Kn,g.fn.tab.noConflict=function(){return g.fn.tab=Nn,Kn._jQueryInterface};var Qn="toast",Bn="bs.toast",Vn="."+Bn,Yn=g.fn[Qn],zn={CLICK_DISMISS:"click.dismiss"+Vn,HIDE:"hide"+Vn,HIDDEN:"hidden"+Vn,SHOW:"show"+Vn,SHOWN:"shown"+Vn},Xn="fade",$n="hide",Gn="show",Jn="showing",Zn={animation:"boolean",autohide:"boolean",delay:"number"},ti={animation:!0,autohide:!0,delay:500},ei='[data-dismiss="toast"]',ni=function(){function i(t,e){this._element=t,this._config=this._getConfig(e),this._timeout=null,this._setListeners()}var t=i.prototype;return t.show=function(){var t=this;g(this._element).trigger(zn.SHOW),this._config.animation&&this._element.classList.add(Xn);var e=function(){t._element.classList.remove(Jn),t._element.classList.add(Gn),g(t._element).trigger(zn.SHOWN),t._config.autohide&&t.hide()};if(this._element.classList.remove($n),this._element.classList.add(Jn),this._config.animation){var n=_.getTransitionDurationFromElement(this._element);g(this._element).one(_.TRANSITION_END,e).emulateTransitionEnd(n)}else e()},t.hide=function(t){var e=this;this._element.classList.contains(Gn)&&(g(this._element).trigger(zn.HIDE),t?this._close():this._timeout=setTimeout(function(){e._close()},this._config.delay))},t.dispose=function(){clearTimeout(this._timeout),this._timeout=null,this._element.classList.contains(Gn)&&this._element.classList.remove(Gn),g(this._element).off(zn.CLICK_DISMISS),g.removeData(this._element,Bn),this._element=null,this._config=null},t._getConfig=function(t){return t=l({},ti,g(this._element).data(),"object"==typeof t&&t?t:{}),_.typeCheckConfig(Qn,t,this.constructor.DefaultType),t},t._setListeners=function(){var t=this;g(this._element).on(zn.CLICK_DISMISS,ei,function(){return t.hide(!0)})},t._close=function(){var t=this,e=function(){t._element.classList.add($n),g(t._element).trigger(zn.HIDDEN)};if(this._element.classList.remove(Gn),this._config.animation){var n=_.getTransitionDurationFromElement(this._element);g(this._element).one(_.TRANSITION_END,e).emulateTransitionEnd(n)}else e()},i._jQueryInterface=function(n){return this.each(function(){var t=g(this),e=t.data(Bn);if(e||(e=new i(this,"object"==typeof n&&n),t.data(Bn,e)),"string"==typeof n){if("undefined"==typeof e[n])throw new TypeError('No method named "'+n+'"');e[n](this)}})},s(i,null,[{key:"VERSION",get:function(){return"4.3.1"}},{key:"DefaultType",get:function(){return Zn}},{key:"Default",get:function(){return ti}}]),i}();g.fn[Qn]=ni._jQueryInterface,g.fn[Qn].Constructor=ni,g.fn[Qn].noConflict=function(){return g.fn[Qn]=Yn,ni._jQueryInterface},function(){if("undefined"==typeof g)throw new TypeError("Bootstrap's JavaScript requires jQuery. jQuery must be included before Bootstrap's JavaScript.");var t=g.fn.jquery.split(" ")[0].split(".");if(t[0]<2&&t[1]<9||1===t[0]&&9===t[1]&&t[2]<1||4<=t[0])throw new Error("Bootstrap's JavaScript requires at least jQuery v1.9.1 but less than v4.0.0")}(),t.Util=_,t.Alert=p,t.Button=P,t.Carousel=lt,t.Collapse=bt,t.Dropdown=Jt,t.Modal=ve,t.Popover=sn,t.Scrollspy=Dn,t.Tab=Kn,t.Toast=ni,t.Tooltip=Be,Object.defineProperty(t,"__esModule",{value:!0})});
//# sourceMappingURL=bootstrap.min.js.map
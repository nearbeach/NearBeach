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


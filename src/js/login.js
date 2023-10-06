//SCSS Library
import "../sass/login.scss";

// Import all of Bootstrap's JS
// import * as bootstrap from 'bootstrap'
// import { Carousel } from 'bootstrap'; //working

//Get an image number
const image_number = Math.floor(Math.random() * 53 + 1);

//Get the background element
const elem = document.getElementsByClassName("background")[0]; //Always the first element

//Get the static directory location
const static_elem = document.getElementById("login_script").dataset.static;

//Apply WebP image
elem.style[
    "background-image"
    ] = `url('${static_elem}NearBeach/images/NearBeach_Background_${image_number.toLocaleString(
    "en",
    {minimumIntegerDigits: 3, useGrouping: false}
)}.webp')`;

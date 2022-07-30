//SCSS Library
import '../sass/login.scss';

//Get an image number
var image_number = Math.floor(Math.random() * 19 + 1);

//Get the background element
var elem = document.getElementsByClassName('background')[0]; //Always the first element

//Get the static directory location
var static_elem = document.getElementById('login_script').dataset.static;

//Apply WebP image
elem.style[
  'background-image'
] = `url('${static_elem}NearBeach/images/NearBeach_Background_${image_number.toLocaleString(
  'en',
  { minimumIntegerDigits: 3, useGrouping: false }
)}.webp')`;
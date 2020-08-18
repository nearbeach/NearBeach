//Import Bootstrap
import { createPopper } from '@popperjs/core';
import bootstrap from 'bootstrap'

//SCSS Library
import '../sass/login.scss';

//Uses to determine if the background can use WebP
function canUseWebP() {
    var elem = document.createElement('canvas');

    if (!!(elem.getContext && elem.getContext('2d'))) {
        // was able or not to get WebP representation
        return elem.toDataURL('image/webp').indexOf('data:image/webp') == 0;
    }

    // very old browser like IE 8, canvas not supported
    return false;
}

//Get an image number
var image_number =  Math.floor((Math.random() * 19) + 1);

//Get the background element
var elem = document.getElementsByClassName('background')[0]; //Always the first element

//Get the extension type
var extension = 'webp';
if (!canUseWebP()) {
    extension = 'jp2';
}

//Set the background-image
elem.style['background-image'] = `url('/static/NearBeach/images/NearBeach_Background_${image_number.toLocaleString('en', {minimumIntegerDigits:3,useGrouping:false})}.${extension}')`;
/*
    This file is part of m.css.

    Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
*/

"use strict"; /* it summons the Cthulhu in a proper way, they say */

let mainView = null;

function flip(id) {
    window.location.hash = '#' + id;

    /* This is the main view, send the change to the presenter window as well */
    if(window.opener)
        window.opener.location.hash = '#' + id;

    /* This is the presenter view */
    else {
        /* Send the change to the main view as well */
        if(mainView && !mainView.closed) {
            mainView.location.hash = '#' + id;

        /* Otherwise update the connection status */
        } else {
            mainView = null;
            let status = document.getElementById('main-view-connection-status');
            if(status) {
                status.innerHTML = 'disconnected';
                status.className = 'm-text m-danger';
            }
        }
    }
}

/* Flipping: when editing, the titles can change and then locating the current
   slide won't work anymore. Prev then jumps to the cover page, next to a page
   right after cover. */

function flipPrev() {
    let current = document.getElementById(window.location.hash.substr(1));
    if(current) {
        let prev = current.previousElementSibling;
        if(prev && prev.id && prev.tagName == 'SECTION') flip(prev.id);
    } else flip("cover");
}

function flipNext() {
    let current = document.getElementById(window.location.hash.substr(1));
    if(!current) current = document.getElementById("cover");
    let next = current.nextElementSibling;
    if(next && next.id && next.tagName == 'SECTION') flip(next.id);
}

document.addEventListener('keydown', function(event) {
    /* TODO home key for the first slide (what is the first?) */

    /* Just opened, flip to cover */
    if(!window.location.hash && (event.key == 'ArrowLeft' || event.key == 'ArrowRight'))
        flip('cover');

    /* Flip to previous */
    else if(event.key == 'ArrowLeft') flipPrev();

    /* Flip to next */
    else if(event.key == 'ArrowRight') flipNext();
});

let touchStart = null;

document.addEventListener('touchstart', function(event) {
    touchStart = event.touches.length == 1 ? event.touches.item(0).clientX : null;
});

document.addEventListener('touchend', function(event) {
    var offset = 100;

    if(touchStart) {
        let end = event.changedTouches.item(0).clientX;

        /* Just opened, flip to cover */
        if(!window.location.hash && (end > touchStart + offset || end < touchStart - offset))
            flip('cover');

        /* Flip to previous */
        else if(end > touchStart + offset) flipPrev();

        /* FLip to next */
        else if(end < touchStart - offset) flipNext();
    }

    touchStart = null;
});

function openMainView(link) {
    mainView = window.open(link.getAttribute('href'), "main-view");
    let status = document.getElementById('main-view-connection-status');
    if(status) {
        status.innerHTML = 'connected';
        status.className = 'm-text m-success';
    }
    return false;
}
